#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent

"""
Intruductory View content
"""
class TVCIntro(TkinterViewContent):

    def show(self, parent):
        # Create widgets
        my_label = Tk.Label(parent, text="Welcome. Press Enter or Space to start the test, F for fullscreen or Esc to exit ")

        # Show widgets
        my_label.pack()
