#!/usr/bin/python2

from typing import Optional, Dict, List, Callable

"""
Current list of commands (event names) for CSPresenter:
- "action"
- "action_alt"
- "back"
Another examples: "move", etc. - generalized input actions applicable on multiple platforms
"""


"""
CSEventSystem sets up an environment for an event invoker / event listener relationship.
Here it is used to let app logic listen and react to events happening in the UI layer (Tkinter) while
maintaining their separation / independecy.
It is an alternative to directly calling app logic functions from the UI layer, which would 1) make them dependent
on each other and 2) create a circular dependency (app calls UI to set it, UI calls app because of input).
Based on: https://stackoverflow.com/questions/6158602/does-python-classes-support-events-like-other-languages
"""
class CSEventSystem:
    def __init__(self):
        self._callbacks = {}  # type: Dict[str, List[Callable]]
        # self._onetime_callbacks = {}  # type: Dict[str, List[Callable]]

    # public
    # Registers a function to be called when the specified event_name is triggered by window or content.
    def add_callback(self, event_name, callback):
        if event_name not in self._callbacks:
            self._callbacks[event_name] = [callback]
        else:
            self._callbacks[event_name].append(callback)
        # print("[add_callback] Registered a callback for event '" + event_name + "'")

    # public
    # Removes a registered callback of a specified event_name
    def remove_callback(self, event_name, callback):
        # type: (str, Callable) -> None
        if event_name not in self._callbacks:
            print("[remove_callback] No event '" + event_name + "' registered")
        elif callback not in self._callbacks[event_name]:
            print("[remove_callback] Specified callback not registered for event '" + event_name + "'")
        else:
            self._callbacks[event_name].remove(callback)
            # print("[remove_callback] Removed a callback for event '" + event_name + "'")

    # public
    # Removes all registered callbacks of a given event_name
    def remove_callbacks(self, event_name):
        if event_name not in self._callbacks:
            print("[remove_callbacks] No event '" + event_name + "' registered")
        else:
            self._callbacks.pop(event_name)
            # print("[remove_callbacks] Removed all callbacks for event '" + event_name + "'")

    # public
    # Removes all registered callbacks
    def remove_all_callbacks(self):
        self._callbacks.clear()
        # print("[remove_all_callbacks] Removed all callbacks")

    # public
    # Calls all the functions registered for event_name.
    # Allows to pass any number of arguments to the called functions.
    # *args and **kwargs explanation here https://realpython.com/python-kwargs-and-args/
    def trigger(self, event_name, *args, **kwargs):
        # normal callbacks
        if event_name not in self._callbacks or not self._callbacks[event_name]:
            print("[trigger] Event '" + event_name + "' triggered without listeners")
        else:
            to_call = list(self._callbacks[event_name])  # type: List
            for callback in to_call:
                print("[trigger] Event '" + event_name + "' triggered")
                callback(*args, **kwargs)

# TODO probably change from list of callbacks to only one callback per trigger allowed to be registered at a time

        # # onetime callbacks with their removal
        # to_call_onetime = list(self._onetime_callbacks.pop(event_name))  # type: List
        # if event_name not in self._onetime_callbacks:
        #     print("[trigger] Event '" + event_name + "' triggered onetime without listeners")
        # else:
        #     for onetime_callback in to_call_onetime:
        #         print("[trigger] Event '" + event_name + "' triggered onetime")
        #         onetime_callback(*args, **kwargs)


    # # public
    # # Registers a one-time callback, that will be called only after the first event and then removed
    # def add_onetime_callback(self, event_name, callback):
    #     if event_name not in self._callbacks:
    #         self._callbacks[event_name] = [callback]
    #     else:
    #         self._callbacks[event_name].append(callback)
    #     print("[add_callback] Registered a one time callback for event '" + event_name + "'")

