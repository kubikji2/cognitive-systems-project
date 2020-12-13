#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent
import random as rnd


"""
Specified number displayed
"""
class TVCNumber(TkinterViewContent):

    def __init__(self):
        self.number = 0

    def show(self, parent):
        # Create widgets

        my_label = Tk.Label(parent, text=str(self.number))
        # my_label.config(font=("Arial", rnd.randrange(26, 48)))
        my_label.config(font=("Arial",  48))
        # Show widgets
        my_label.pack()

    def set_data(self, data):
        self.number = data
