#!/usr/bin/python2

import Tkinter as Tk
from typing import Optional, Callable, Dict, Union
from CSEventSystem import CSEventSystem
from CSViewContent import CSViewContent
from CSVCGeneral import CSVCGeneral
from CSVCIntro import CSVCIntro
from CSVCNumber import CSVCNumber
from CSVCImage import CSVCImage
from CSVCResults import CSVCResults

MOUSE_LABEL = "<Button-1>"

"""
CSView (Cognitive Systems View) is a class providing methods for viewing content to the user and getting input. 
Specifically, it is currently implemented using Tkinter library, creating and maintaining a window on desktop.
TODO Possibly rather make an interface for view, and make this class a concrete Tkinter view implementation of it.
Inside CSView the current CSViewContent is drawn (see CSViewContent class for futher details).
CSView takes care of propagating user inputs (events) to the CSViewContent via binding and unbinding them 
and also redrawing whether new content is set via set_content method.
"""
class CSView:

    def __init__(self, cs_event_system):
        # type: (CSEventSystem) -> None

        # manage keyboard and mouse input
        self.cs_event_system = cs_event_system  # type: CSEventSystem
        self._set_window()
        self._set_frame()
        self._content = None  # type: Optional[CSViewContent]  # current viewing and input content
        self._base_input_content = None  # type: Optional[CSViewContent]  # current additional (general) input content
        self._time_multiplier = 1

        # view content cache -> faster changes in view (specifically because of image loading)
        self._csvc_cache = {}  # type: Dict[Union[str, int], CSViewContent]
        self._csvc_cache["general_input"] = CSVCGeneral(self)
        self._csvc_cache["intro"] = CSVCIntro(self)
        self._csvc_cache["mask"] = CSVCImage(self, "mask.png")
        self._csvc_cache["response"] = CSVCImage(self, "response.png")
        self._csvc_cache["fixation"] = CSVCImage(self, "fixation.png")
        for i in range(1, 10):
            self._csvc_cache[i] = CSVCNumber(self, i)
        self._csvc_cache["results"] = CSVCResults(self)

    # private
    # set up window
    def _set_window(self):
        # init root window
        self.window = Tk.Tk()  # window reference should only be GET from other classes, never SET!
        self.window.geometry("800x600")
        # self.window.eval('tk::PlaceWindow . center')  # place the windowed version to center of screen
        # self.window.attributes('-fullscreen', True)
        self.window.title("SART test")
        self.window.tk_setPalette(background="black", foreground="white")

    # private
    # prepare frame 
    def _set_frame(self):
        self.frame = Tk.Frame(self.window)
        self.frame.place(relx=.5, rely=.5, anchor="center")

    # public
    # Begin the window refresh and input loop
    def run(self):
        self.window.mainloop()

    # public
    # set to view a specified CSWindow Content that is stored in cache under content_name
    # '-> unbind previous input control
    # '-> set new content
    # '-> clear frame
    # '-> bind new input control
    def set_content(self, content_name):
        # type: (CSView, Union[str, int]) -> None

        if self._content is not None:
            self._content.unbind()
        if content_name in self._csvc_cache:
            self._content = self._csvc_cache[content_name]
            self.clear_content()
            self._content.bind()
            self._content.show()
        else:
            print ("[view] ERROR: specified view content '" + str(content_name) + "' not found")

    # public
    # only take and bind input keys from a specified content CSWindow Content
    # '-> unbind previous input control
    # '-> bind new input control
    # TODO: probably could be done in a better way
    def set_base_input_content(self, content_name):
        # type: (CSView, Union[str, int]) -> None

        if self._base_input_content is not None:
            self._base_input_content.unbind()
        if content_name in self._csvc_cache:
            self._base_input_content = self._csvc_cache[content_name]
            self._base_input_content.bind()
        else:
            print ("[view] ERROR: specified input content '" + str(content_name) + "' not found")

    # public
    # clears frame from any content
    # '-> destroy all widgets
    # '-> TODO: clear all drawn elements too maybe?
    # based on:
    # https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
    def clear_content(self):
        # destroy all widgets from frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        self.frame.pack_forget()

    # public
    # Sets a timer which raises a "timeout" event after a set period of time
    # Can be extended to cancelling functionality https://stackoverflow.com/questions/53756018/after-cancel-method-tkinter
    def set_timer(self, ms, callback):
        # type: (int, Callable) -> None
        self.window.after(ms * self._time_multiplier, callback)
        # print("[set_timer] " + str(ms * self._time_multiplier))

    # public
    def toggle_fullscreen(self):
        self.window.attributes("-fullscreen", not self.window.attributes("-fullscreen"))

    # public
    # Ends mainloop and destroys the whole window - if nothing else is actively running, this is the end for the whole app
    def close(self):
        self.window.destroy()

    # public
    # mostly for debugging puroposes - multiplies every waiting time by specified number
    def warp_time(self, multiplier):
        self._time_multiplier = multiplier
