#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent


"""
Outro screen with options to redo the test or show results
"""
class TVCOutro(TkinterViewContent):

    def show(self, parent):
        # Create widgets
        my_label = Tk.Label(parent, text="Congratulations on finishing the test!")
        my_label2 = Tk.Label(parent, text="Press space/enter to show results")

        # Show widgets
        my_label.pack()
        my_label2.pack()
