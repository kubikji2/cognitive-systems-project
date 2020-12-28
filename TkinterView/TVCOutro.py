#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent


"""
Outro screen with options to redo the test or show results
"""
class TVCOutro(TkinterViewContent):

    def show(self, parent):
        # Create widgets
        lbl_congrats = Tk.Label(parent, text="Congratulations on finishing the test!", font=("Arial", 16))
        lbl_saved = Tk.Label(parent, text="Your result was saved on disk")
        lbl_ctrl_1 = Tk.Label(parent, text="Press space/enter to view your result")
        lbl_ctrl_2 = Tk.Label(parent, text="Press R to go back to intro")
        lbl_ctrl_3 = Tk.Label(parent, text="Press Esc to exit")

        # Show widgets
        lbl_congrats.pack()
        lbl_saved.pack(pady=(0, 10))
        lbl_ctrl_1.pack()
        lbl_ctrl_2.pack()
        lbl_ctrl_3.pack()
