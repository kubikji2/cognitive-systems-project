#!/usr/bin/python2

from Tkinter import *

from CSWindow import CSWindow
from CSWindowContent import CSWindowContent

# Just testing content feel free to do whatever you want to
class CSWCTest(CSWindowContent):
    def __init__(self, window):
        # base constructor call
        # it requires list of the keys to listen
        CSWindowContent.__init__(self, window, ["a","s","d","w","<Return>"])

        print(self.window)
        
    def draw(self):
        # Create widgets
        # frame je vlastne jen seskupovac vicero widgetu ktere tvori nejaky celek, abych s nimi mohl napr hybat najednou
        my_label = Label(self.cs_window.frame, text="Hello world")

        # Show widgets
        self.cs_window.frame.place(relx=.5, rely=.5, anchor="center")
        my_label.pack()
        

    def key_callback(self, event):
        print("key: " + event.char)

    def mouse_callback(self,event):
        print("mouse clicked at ["+str(event.x)+","+str(event.y)+"]")
