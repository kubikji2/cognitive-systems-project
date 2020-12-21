#!/usr/bin/python2

import TkinterView as Tk
from typing import Optional, Callable, Dict, Union, Any
from CSEventSystem import CSEventSystem
from CSData import CSData

"""
CSView (Cognitive Systems View) is an abstract-like class providing methods for viewing content to the user and getting input. 
It is supposed to be implemented using Tkinter for pc and ??? for Pepper humanoid-robot
"""
class CSView:

    def __init__(self, cs_event_system):
        # type: (CSEventSystem) -> None
        # register event system for raising events in it
        self.cs_event_system = cs_event_system  # type: CSEventSystem
        # self.cs_data = cs_data  # type: CSData

    # public
    # Begin the window refresh and input loop
    def run(self):
        print("TBD")

    # public
    # set to view a specified view content
    def set_content(self, content_name, data=None):
        # type: (str, Any) -> None
        print("TBD")

    # public
    # clears view
    def clear_content(self):
        print("TBD")

    # public
    # specific views can have user to create a more compicated input (eg getting a whole word using text or speech)
    # this method gets this complex info from what is currently viewed (should return None if nothing to be read)
    def read_input(self):
        # type: () -> Any
        print("TBD")

    # public
    # Sets a timer which calls the specified function after set time
    def set_timer(self, ms, callback):
        print("TBD")

    # public
    # closes the app
    def close(self):
        print("TBD")

    # public
    # mostly for debugging puroposes - multiplies every waiting time by specified number
    def warp_time(self, multiplier):
        print("TBD")
