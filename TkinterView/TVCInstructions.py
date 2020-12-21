#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent

"""

"""
class TVCInstructions(TkinterViewContent):

    def show(self, parent):
        # Create widgets
        lbl_header = Tk.Label(parent, text="Instructions", font=("Arial", 30))
        lbl_instructions = Tk.Message(parent, width=600, font=("Arial", 12), justify=Tk.CENTER, text="""
In this experiment you will be presented with digits 1 to 9 in the center of the screen. The digits will be presented in sequential order and repeated multiple times. Your task is to press Enter or Space in response to each digit, except for when the digit is a '3'.

For example, if you see the digit '1', press the spacebar. If you see the digit '3', DO NOT press the spacebar.

Each digit will be followed by a circle with a cross. The cross will then blink bold, which indicates when you should respond to the digit you just saw. You should not respond before the cricle appears - try to respond exactly on the indication, not sooner, nor later. Lastly, there will be a simple cross without circle marking preparation time for next digit.
        """)
        lbl_controls1 = Tk.Label(parent, font=("Arial", 16), text="Press Enter or Space to start a training block")
        lbl_controls2 = Tk.Label(parent, text="Press R to skip training")
        lbl_controls3 = Tk.Label(parent, text="Press Esc to go back to intro")

        # Place widgets
        lbl_header.grid(row=0, pady=(0, 10))
        lbl_instructions.grid(row=1, pady=(0, 30))
        lbl_controls1.grid(row=2)
        lbl_controls2.grid(row=3)
        lbl_controls3.grid(row=4)
