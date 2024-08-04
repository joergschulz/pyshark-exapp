#!/usr/bin/env python

import asyncio
import signal

import threading
import tkinter
import tkinter.ttk

from ._vendor import pyshark


c = pyshark.LiveCapture(interface='lo', bpf_filter='icmp', debug=True)
# das hier wäre noch etwas "sauberer" benötigt aber den "add interface option to Capture base-class" patch aus test1 branch
#c = Capture(interface='bresp42', capture_filter='icmp', debug=True)

capture_paused = False

def win():
    root = tkinter.Tk()

    def start_stop():
        global capture_paused
        capture_paused = not capture_paused

    def quit():
        root.destroy()
        asyncio.run_coroutine_threadsafe(c.close_async(), c.eventloop)

    frm = tkinter.ttk.Frame(root, padding=10)
    frm.grid()
    tkinter.ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    tkinter.ttk.Button(frm, text="Start/Stop", command=start_stop).grid(column=1, row=0)
    tkinter.ttk.Button(frm, text="Quit", command=quit).grid(column=2, row=0)
    root.mainloop()


i=0
async def packet_print(p):
    global i
    if capture_paused:
        return
    i=i+1
    print(f'packet {i}')

def capture():
    c.apply_on_packets( packet_print )

def main():
    print('Hello')
    print(pyshark.__path__)

    # thread_gui = threading.Thread( target=win )
    # thread_gui.start()
    # thread_gui.join()

    thread_capture = threading.Thread( target=capture )
    thread_capture.start()
    win()
    thread_capture.join()

