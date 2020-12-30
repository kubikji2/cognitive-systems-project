#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent
from typing import List
from CSData import CSData, WHOLE

"""

"""
class TVCTutorialResults(TkinterViewContent):

    def __init__(self):
        self._total_errors = 0  # type: int
        self._steps = 0  # type: int

    def show(self, parent):
        # Create widgets
        lbl_header = Tk.Label(parent, text=("You did " + str(self._total_errors) + " errors during " + str(self._steps) + " trials of the training block."), font=("Arial", 16))

        lbl_controls1 = Tk.Label(parent, text="Press Enter or Space to begin the real test", font=("Arial", 24))
        lbl_controls2 = Tk.Label(parent, text="Press R to try the training again")
        lbl_controls3 = Tk.Label(parent, text="Press Esc to go back to intro")


        # Place widgets
        lbl_header.grid(row=0, pady=(0, 5))
        lbl_controls1.grid(row=1)
        lbl_controls2.grid(row=2)
        lbl_controls3.grid(row=3)

    def set_data(self, data):
        # type: (CSData) -> None
        self._total_errors = data.get_total_errors()[WHOLE]
        self._steps = data.step_count[WHOLE]
