from typing import Optional, Dict, List, Callable

"""
Current list of commands (event names) for CSPresenter:
- "action"
- "action_alt"
- "back"
- "right"
- "left"
- "any"
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
        self._callbacks = {}  # type: Dict[str, Callable]
        self._onetime_callbacks = {}  # type: Dict[str, Callable]

    # public
    # Registers a function to be called when the specified event_name is triggered by window or content.
    # It overwrites any previously registered function for this event
    def add_callback(self, event_name, callback):
        # type: (str, Callable) -> None
        # if event_name not in self._callbacks:
        #     print("[add_callback] Registered a callback for event '" + event_name + "'")
        # else:
        #     print("[add_callback] WARN Overwritten a callback for event '" + event_name + "'")
        self._callbacks[event_name] = callback

    # public
    # Registers a one-time function, that will be called only after the first event and then removed
    def add_onetime_callback(self, event_name, callback):
        # type: (str, Callable) -> None
        # if event_name not in self._callbacks:
        #     print("[add_onetime_callbacks] Registered a one-time callback for event '" + event_name + "'")
        # else:
        #     print("[add_onetime_callback] WARN Overwritten a one-time callback for event '" + event_name + "'")
        self._onetime_callbacks[event_name] = callback

    # public
    # Removes the registered callback of the specified event_name
    def remove_callback(self, event_name):
        # type: (str) -> None
        # if event_name not in self._callbacks:
        #     print("[remove_callback] WARN No event '" + event_name + "' registered")
        # else:
        #     print("[remove_callback] Removed a callback for event '" + event_name + "'")
        self._callbacks.pop(event_name, None)

    # public
    # Removes the registered callback of the specified event_name
    def remove_onetime_callback(self, event_name):
        # type: (str) -> None
        # if event_name not in self._callbacks:
        #     print("[remove_callback] WARN No event '" + event_name + "' registered")
        # else:
        #     print("[remove_callback] Removed a callback for event '" + event_name + "'")
        self._onetime_callbacks.pop(event_name, None)

    # public
    # Removes all registered callbacks
    def remove_all_callbacks(self):
        self._callbacks.clear()
        self._onetime_callbacks.clear()
        # print("[remove_all_callbacks] Removed all callbacks")

    # public
    # Calls the function registered for event_name.
    # Allows to pass any number of arguments to the called function.
    # *args and **kwargs explanation here https://realpython.com/python-kwargs-and-args/
    def trigger(self, event_name, *args, **kwargs):
        if event_name not in self._callbacks and event_name not in self._onetime_callbacks:
            # print("[trigger] WARN Event '" + event_name + "' triggered without listeners")
            pass
        # one-time callbacks
        elif event_name in self._onetime_callbacks:  # onetime callbacks take priority over normal ones
            # print("[trigger] Event '" + event_name + "' triggered one-time")
            to_call = self._onetime_callbacks.pop(event_name)  # remove the callback from the list
            to_call(*args, **kwargs)  # call the registered function
        # normal callbacks
        else:
            # print("[trigger] Event '" + event_name + "' triggered")
            self._callbacks[event_name](*args, **kwargs)  # call the registered function



