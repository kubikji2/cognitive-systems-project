#!/usr/bin/python2

from Tkinter import *
from CSWindowContent import CSWindowContent
from CSWCTest import CSWCTest

"""
Intruductory Windows content
"""
class CSWCIntro(CSWindowContent):

    def __init__(self, cs_window):
        # base constructor call
        # it requires list of the keys to listen
        CSWindowContent.__init__(self, cs_window, ["t"])

        print("window", self.window, cs_window)
        
    def draw(self):
        # Create widgets
        my_label = Label(self.cs_window.frame, text="Welcome. Press Enter (TBD) to continue, Esc to exit, T for testing context")

        # Show widgets
        self.cs_window.frame.place(relx=.5, rely=.5, anchor="center")
        my_label.pack()

    def key_callback(self, event):
        print("key: " + event.char)
        if(event.char == "t"):
            self.cs_window.set_content(CSWCTest(self.cs_window))

    def mouse_callback(self,event):
        print("mouse clicked at ["+str(event.x)+","+str(event.y)+"]")