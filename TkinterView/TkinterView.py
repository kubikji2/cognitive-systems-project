#!/usr/bin/python2

# btw avoiding cyclic dependecy in type hints using https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports
# general info for type hints in Python 2.7 https://www.python.org/dev/peps/pep-0484/

import Tkinter as Tk
from typing import Optional, Callable, Dict, Union, Any
from CSEventSystem import CSEventSystem
from CSData import CSData
from CSView import CSView
from TkinterViewContent import TkinterViewContent
from TVCIntro import TVCIntro
from TVCNumber import TVCNumber
from TVCImage import TVCImage
from TVCOutro import TVCOutro
from TVCResults import TVCResults

"""
TkinterView (implementing CSView) is a class providing methods for viewing content to the user and getting input. 
It is implemented using Tkinter library, creating and maintaining a window on desktop.
Inside TkinterView the current TkinterViewContent is drawn (see the class for futher details).
TkinterView takes care of propagating user inputs (events) to the TkinterViewContent via binding and unbinding them 
and also redrawing whether new content is set via set_content method.
"""
class TkinterView(CSView):

    def __init__(self, cs_event_system, cs_data):
        # type: (CSEventSystem, CSData) -> None
        CSView.__init__(self, cs_event_system, cs_data)

        # set up window and frame
        self._set_window()
        self._set_frame()
        self._content = None  # type: Optional[TkinterViewContent]  # current viewing and input content
        self._time_multiplier = 1

        # set up keyboard input
        self._key_event_map = {}  # type: Dict[str, str]
        self._key_event_map["<Return>"] = "action"
        self._key_event_map["<space>"] = "action"
        self._key_event_map["<Escape>"] = "back"
        self._key_event_map["<BackSpace>"] = "back"
        self._key_event_map["r"] = "action_alt"
        self._key_event_map["f"] = "fullscreen"
        self._char_key_map = {}
        self._char_key_map["\r"] = "<Return>"
        self._char_key_map[" "] = "<space>"
        self._char_key_map["\x1b"] = "<Escape>"
        self._char_key_map["\b"] = "<BackSpace>"
        self._char_key_map["r"] = "r"
        self._char_key_map["f"] = "f"
        self._key_fids = []
        self._bind_keyboard_input()

        # view content cache -> faster changes in view (specifically because of image loading)
        self._vc_cache = {}  # type: Dict[Union[str, int], TkinterViewContent]
        self._vc_cache["intro"] = TVCIntro()
        self._vc_cache["mask"] = TVCImage("Images/mask.png")
        self._vc_cache["response"] = TVCImage("Images/response.png")
        self._vc_cache["fixation"] = TVCImage("Images/fixation.png")
        self._vc_cache["number"] = TVCNumber()
        self._vc_cache["outro"] = TVCOutro()
        self._vc_cache["results"] = TVCResults()

# private
    # set up window
    def _set_window(self):
        # init root window
        self._window = Tk.Tk()  # window reference should only be GET from other classes, never SET!
        self._window.geometry("800x600")
        # self.window.eval('tk::PlaceWindow . center')  # place the windowed version to center of screen
        # self.window.attributes('-fullscreen', True)
        self._window.title("SART test")
        self._window.tk_setPalette(background="black", foreground="white")

    # prepare frame 
    def _set_frame(self):
        self._frame = Tk.Frame(self._window)
        self._frame.place(relx=.5, rely=.5, anchor="center")


    # map keyboard and mouse input to events
    # key binding reference https://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding
    def _bind_keyboard_input(self):
        for key, event in self._key_event_map.items():
            fid = self._window.bind(key, lambda keyboard_event: self._key_callback(keyboard_event))
            self._key_fids.append(fid)

    # unbind keyboard
    def _unbind_keyboard_input(self):
        keys = self._key_event_map.keys()
        for i in range(len(keys)):
            key = keys[i]
            fid = self._key_fids[i]
            self._window.unbind(key, fid)

    # a function to be called by Tkinter when specified keys are pressed
    def _key_callback(self, keyboard_event):
        key = self._char_key_map[keyboard_event.char]
        event = self._key_event_map[key]
        # print("key: " + repr(key))
        if event == "fullscreen":
            self._toggle_fullscreen()
        else:
            self.cs_event_system.trigger(event)

    # Tkinter view specific command to go fullscreen
    def _toggle_fullscreen(self):
        self._window.attributes("-fullscreen", not self._window.attributes("-fullscreen"))

# public
    # Begin the window refresh and input loop
    def run(self):
        self._window.mainloop()

    # set to view a specified CSWindow Content that is stored in cache under content_name
    # '-> unbind previous input control
    # '-> set new content
    # '-> clear frame
    # '-> bind new input control
    def set_content(self, content_name, data=None):
        # type: (str, Any) -> None
        if content_name in self._vc_cache:
            self.clear_content()
            self._content = self._vc_cache[content_name]
            if data is not None:
                self._content.set_data(data)
            self._content.show(self._frame)
        else:
            print ("[view] ERROR: specified view content '" + str(content_name) + "' not found")

    # clears frame from any content
    # '-> destroy all widgets
    # '-> TODO: clear all drawn elements too maybe?
    # based on:
    # https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
    def clear_content(self):
        # destroy all widgets from frame
        for widget in self._frame.winfo_children():
            widget.destroy()
        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        self._frame.pack_forget()
        self._content = None

    # Sets a timer which raises a "timeout" event after a set period of time
    # Can be extended to cancelling functionality https://stackoverflow.com/questions/53756018/after-cancel-method-tkinter
    def set_timer(self, ms, callback):
        # type: (int, Callable) -> None
        self._window.after(ms * self._time_multiplier, callback)
        # print("[set_timer] " + str(ms * self._time_multiplier))

    # Ends mainloop and destroys the whole window - if nothing else is actively running, this is the end for the whole app
    def close(self):
        self._window.destroy()

    # mostly for debugging puroposes - multiplies every waiting time by specified number
    def warp_time(self, multiplier):
        self._time_multiplier = multiplier
