#!/usr/bin/python2

import Tkinter as Tk
from typing import Optional, Callable
from CSEventSystem import CSEventSystem
from CSViewContent import CSViewContent

MOUSE_LABEL = "<Button-1>"

"""
CSWindow (Cognitive Systems View) creates a Tkinter window.
Inside CSView the current CSViewContent is drawn (see CSViewContent class for futher details).
CSView takes care of propagating user inputs (events) to the CSViewContent via binding and unbinding them and also redrawing whether new content is set via set_content method.
"""
class CSView:

    def __init__(self, cs_event_system):
        # type: (CSEventSystem) -> None

        # manage keyboard and mouse input
        self.cs_event_system = cs_event_system  # type: CSEventSystem
        self._set_window()
        self._set_frame()
        self._content = None  # type: Optional[CSViewContent]
        self._base_input_content = None  # type: Optional[CSViewContent]
        self._time_multiplier = 1

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
    # set new CSWindow Content
    # '-> unbind previous input control
    # '-> set new content
    # '-> clear frame
    # '-> bind new input control
    # TODO: rework unbind/bind so that its quick in succession (no timewindow without input), mybe even check for same binding?
    def set_content(self, content):
        # type: (CSView, CSViewContent) -> None

        if self._content is not None:
            self._content.unbind()
        self._content = content
        self.clear_content()
        self._content.bind()
        self._content.show()

    # public
    # take and bind keys from specified content CSWindow Content
    # '-> unbind previous input control
    # '-> bind new input control
    # TODO: probably could be done better way?
    def set_base_input_content(self, content):
        # type: (CSView, CSViewContent) -> None

        if self._base_input_content is not None:
            self._base_input_content.unbind()
        self._base_input_content = content
        self._base_input_content.bind()

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
