#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent


"""
Screen showing the results to the user
"""
class TVCResults(TkinterViewContent):

    def __init__(self):
        pass

    def show(self, parent):
        # Create widgets
        my_label = Tk.Label(parent, text="Your results were saved on disk, here you can view them")
        my_label2 = Tk.Label(parent, text="Press R to try again or esc/backspace quit")

        # Show widgets
        my_label.pack()
        my_label2.pack()

    def set_data(self, data):
        pass

