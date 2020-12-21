#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent


"""
Get ready phrase 
"""
class TVCReady(TkinterViewContent):

    def show(self, parent):
        # Create widgets
        my_label = Tk.Label(parent, text="Get ready...", font=("Arial", 16))

        # Place widgets
        my_label.pack()
