#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent
import random as rnd


"""
Specified number displayed
"""
class TVCNumber(TkinterViewContent):

    def __init__(self, cs_view, number=0):
        # base constructor call
        # it requires list of the keys to listen
        TkinterViewContent.__init__(self, cs_view)
        # set this content's parameters
        self.number = number

    def show(self):
        # Create widgets

        my_label = Tk.Label(self.csv.frame, text=str(self.number))
        # my_label.config(font=("Arial", rnd.randrange(26, 48)))
        my_label.config(font=("Arial",  48))
        # Show widgets
        my_label.pack()

    def key_callback(self, event):
        pass

    def mouse_callback(self, event):
        pass
