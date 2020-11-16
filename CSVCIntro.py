#!/usr/bin/python2

import Tkinter as Tk
from CSViewContent import CSViewContent

"""
Intruductory View content
"""
class CSVCIntro(CSViewContent):

    def __init__(self, cs_view):
        # base constructor call
        # it requires list of the keys to listen
        CSViewContent.__init__(self, cs_view)

    def show(self):
        # Create widgets
        my_label = Tk.Label(self.csv.frame, text="Welcome. Press Enter or Space to start the test, F for fullscreen or Esc to exit ")

        # Show widgets
        my_label.pack()

    def key_callback(self, event):
        pass

    def mouse_callback(self, event):
        pass
