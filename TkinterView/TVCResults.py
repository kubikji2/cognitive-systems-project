#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent


"""
Screen showing the results to the user
"""
class TVCResults(TkinterViewContent):

    def __init__(self, cs_view):
        # base constructor call
        # it requires list of the keys to listen
        TkinterViewContent.__init__(self, cs_view, ['r'])

    def show(self):
        # Create widgets
        my_label = Tk.Label(self.csv.frame, text="Here are your results")

        # Show widgets
        my_label.pack()

    def key_callback(self, event):
        if event.char == 'r':
            self.csv.cs_event_system.trigger("action_alt")

    def set_data(self, data):
        pass

