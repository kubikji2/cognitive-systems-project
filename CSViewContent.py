#!/usr/bin/python2

import Tkinter as Tk
from typing import List, Optional
#from CSView import CSView
# avoided cyclic dependecy in type hints using https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports
# general info for type hints in Python 2.7 https://www.python.org/dev/peps/pep-0484/

"""
This abstract-like class take care of content shown in the CSView.
Each inherited class should be named in format CSVC+Name.
If there are any keyboard keys used as input, pass them in the constructor.
"""
class CSViewContent:

    # constructor
    # '-> CSView is required for full control over the window visual
    # '-> List of keys used by the Content is neccessary to set up input handlers
    def __init__(self, cs_view, keys=[]):
        # type: ('CSView', Optional[List[str]]) -> None

        # CSView containing the window I am drawing into
        self.csv = cs_view

        # keys I will be listening to
        self.keys = keys

        # handler function ids, used for unbinding
        # '-> based on:
        #     https://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding
        self.key_fids = []

    # public / do not change in inherited classes!
    # bond inputs to the callbacks
    def bind(self):
        # binding keys
        for i in range(len(self.keys)):
            key = self.keys[i]
            if key == '<Button-1>':
                fid = self.csv.window.bind(key, self.mouse_callback)
            else:
                fid = self.csv.window.bind(key, lambda event: self.key_callback(event))
            self.key_fids.append(fid)

    # public / do not change in inherited classes!
    # removes bond between callbacks and inputs
    def unbind(self):
        # unbind keys
        for i in range(len(self.keys)):
            key = self.keys[i]
            fid = self.key_fids[i]
            self.csv.window.unbind(key, fid)

    # abstract
    # create and show the contents using Tkinter
    def show(self):
        print("TBD")

    # abstract
    # handle keyboard input
    def key_callback(self, event):
        print("TBD")

    # abstract
    # handle mouse input
    # TODO probably need better interface
    def mouse_callback(self, event):
        print("TBD")

    # abstract
    # handle touch screen
    # TODO fix it
    def touch_screen_callback(self, event):
        print("TBD")

    # Not used at the moment
    # hardware abstraction
    def handle_xy(self, x, y):
        print("TBD")
