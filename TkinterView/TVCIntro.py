#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent

"""
Intruductory View content
"""
class TVCIntro(TkinterViewContent):

    def show(self, parent):
        # Create widgets
        lbl_header = Tk.Label(parent, text="Sustained Attention to Response Task", font=("Courier", 30))
        lbl_sub_header = Tk.Label(parent, text="Fixed-sequence", font=("Courier", 14))
        lbl_controls1 = Tk.Label(parent, text="Press Enter or Space to continue to instructions", font=("Arial", 16))
        lbl_controls3 = Tk.Label(parent, text="Press R to show saved results")
        lbl_controls2 = Tk.Label(parent, text="Press F to toggle fullscreen")
        lbl_controls4 = Tk.Label(parent, text="Press Esc to exit")

        # Place widgets
        lbl_header.grid(row=0)
        lbl_sub_header.grid(row=1, pady=(0, 40))
        lbl_controls1.grid(row=2)
        lbl_controls2.grid(row=3)
        lbl_controls3.grid(row=4)
        lbl_controls4.grid(row=5)
