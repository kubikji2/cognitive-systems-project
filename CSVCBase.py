#!/usr/bin/python2

import Tkinter as Tk
from CSViewContent import CSViewContent

"""
Content with base input controls for the Tkinter window and now show method
"""
class CSVCBase(CSViewContent):

    def __init__(self, cs_view):
        # base constructor call
        # it requires list of the keys to listen
        CSViewContent.__init__(self, cs_view, ['f', '<Escape>', '<Return>', '<space>'])

    def key_callback(self, event):
        # print("[CSVCBase] key: " + repr(event.char))
        if event.char == '\r' or event.char == ' ':
            self.csv.cs_event_system.trigger("action")
        elif event.char == '\x1b':
            self.csv.cs_event_system.trigger("back")
        elif event.char == 'f':
            self.csv.toggle_fullscreen()

    def mouse_callback(self, event):
        pass
