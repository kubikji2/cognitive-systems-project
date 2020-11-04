#!/usr/bin/python2

from Tkinter import *

"""
This abstract-like class take care of content shown in the CSWindow.
Each inherited class should be named in format CSWC+Name.
If there are any keyboard keys used as input, pass them in the constructor.
"""
class CSWindowContent:

    # constructor
    # '-> CSWindow is required for full control over the window visual
    # '-> List of keys used by the Content is neccessary to set up input handlers
    def __init__(self, cs_window, keys = []):
        # window I am drawing into
        self.cs_window = cs_window
        self.window = cs_window.window
        
        # keys I will be listening
        self.keys = keys

        # handler function ids, used for unbinding
        # '-> based on:
        #     https://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding
        self.key_fids = []
        self.mouse_fid = -1
    
    # public-like but do not change in inherited classes!
    # bond inputs to the callbacks
    def bind(self):
        # binding mouse
        self.mouse_fid = self.window.bind("<Button-1>", self.mouse_callback)

        # binding keys
        for i in range(len(self.keys)):
            key = self.keys[i]
            fid = self.window.bind(key, lambda event : self.key_callback(event))
            self.key_fids.append(fid)

    # public-like but do not change in inherited classes!
    # removes bond between callbacks and inputs
    def unbind(self):
        # unbind mouse
        self.window.unbind("<Button-1>", self.mouse_fid)

        # unbind keys
        for i in range(len(self.keys)):
            key = self.keys[i]
            fid = self.key_fids[i]
            self.window.unbind(key,fid)

    # abstract-like do whatever you want
    # handle keyboard input
    def key_callback(self, event):
        print("TBD")

    # abstract-like do whatever you want
    # handle mouse input
    # TODO probably need better interface
    def mouse_callback(self,event):
        print("TBD")

    # abstract-like do whatever you want
    # handle touch screen
    # TODO fix it
    def touch_screen_callback(self,event):
        print("TBD")

    # Not used at the moment
    # hardware abstraction
    def handle_xy(self,x,y):
        print("TBD")