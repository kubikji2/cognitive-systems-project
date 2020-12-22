#!/usr/bin/python2

"""
This abstract-like class take care of content shown in the TkinterView.
Each inherited class should be named in format TVC+Name.
"""
class TkinterViewContent:

    # abstract
    # create and show the contents using Tkinter
    def show(self, parent):
        print("TBD")

    # abstract
    # specify data to view
    def set_data(self, data):
        print("TBD")

    # abstract
    # read text input from the user if the current viewcontent has any
    def read_input(self):
        print("TBD")
