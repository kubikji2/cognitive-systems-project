#!/usr/bin/python2

import random as rnd
import time
from typing import Optional

from CSView import CSView
from CSEventSystem import CSEventSystem
from CSData import CSData


"""
CSPresenter (Cognitive Systems Presenter) is a class
- defining the procedure / sequence of actions of the chosen CS test (SART)
- holding information about the current logic state of the application
- listening and reacting to events happening in UI
- controlling what should be currently viewed
- saving/loading information to/from the data class
"""
class CSPresenter:
    def __init__(self, cs_view, cs_event_system):
        # type: (CSView, CSEventSystem) -> None

        print("[app] yay presenter instantiated")
        self._cs_view = cs_view
        self._cs_event_system = cs_event_system

        # SART config
        self._step_count = 5  # type: int
        self._tutorial_step_count = 3  # type: int

        # state holders
        self._current_cs_data = None  # type: Optional[CSData]
        self._username = ""  # type: str
        self._tutorial_test = True  # type: bool
        self._current_step = 0  # type: int
        self._current_number = 0  # type: int
        self._stopwatch_start_time = 0  # type: float  # used as a store for measuring time of user input

    # || The following functions each control a certain logical part/functionality of the app ||

    # --- INTRO ---
    # public
    # Sets up the app and shows it to user
    def start(self):
        self._show_intro()
        self._cs_view.run()
        # self._cs_view.warp_time(2)  # DEBUGGING SETTINGS

    def _show_intro(self):
        self._current_cs_data = None  # just in case
        self._cs_event_system.remove_all_callbacks()
        self._cs_event_system.add_onetime_callback("action", self._show_username_input)
        self._cs_event_system.add_onetime_callback("action_alt", self._show_saved_results)
        self._cs_event_system.add_onetime_callback("back", self._cs_view.close)
        self._cs_view.set_content("intro")

    def _show_username_input(self):
        self._cs_event_system.remove_all_callbacks()
        self._cs_event_system.add_onetime_callback("action", self._get_username_input)
        self._cs_event_system.add_onetime_callback("back", self._show_intro)
        self._cs_view.set_content("username_input")

    def _get_username_input(self):
        username = self._cs_view.read_input()  # type: str
        if not username.isalnum():
            print("[CSPresenter] Please specify a name using a-Z, 0-9")
            self._cs_event_system.add_onetime_callback("action", self._get_username_input)
        else:
            # Create a new instance of user data
            self._username = username
            self._show_instructions()

    def _show_instructions(self):
        self._cs_event_system.remove_all_callbacks()
        self._cs_event_system.add_onetime_callback("action", self._start_tutorial)
        self._cs_event_system.add_onetime_callback("action_alt", self._show_tutorial_results)
        self._cs_event_system.add_onetime_callback("back", self._show_intro)
        self._cs_view.set_content("instructions")

    def _show_tutorial_results(self):
        self._cs_event_system.remove_all_callbacks()
        self._cs_event_system.add_onetime_callback("action", self._start_test)
        self._cs_event_system.add_onetime_callback("action_alt", self._show_instructions)
        self._cs_event_system.add_onetime_callback("back", self._show_intro)
        if self._current_cs_data is not None:
            self._current_cs_data.evaluate_results()
            self._cs_view.set_content("tutorial_results", self._current_cs_data)
        else:
            self._cs_view.set_content("tutorial_results")

    def _show_saved_results(self):
        # todo? multiple instances of CSData
        pass

    # --- TEST SEQUENCE ---
    def _start_tutorial(self):
        self._cs_event_system.remove_all_callbacks()
        self._tutorial_test = True
        self._current_step = 0
        self._current_number = 1
        self._current_cs_data = CSData(step_count=self._tutorial_step_count, name=self._username)
        self._show_ready()

    def _start_test(self):
        self._cs_event_system.remove_all_callbacks()
        self._tutorial_test = False
        self._current_step = 0
        self._current_number = 1
        self._current_cs_data = CSData(step_count=self._step_count, name=self._username)
        self._show_ready()

    def _show_ready(self):
        self._cs_view.set_content("ready")
        self._cs_view.set_timer(1000, self._show_empty)

    def _show_empty(self):
        self._cs_view.clear_content()
        self._cs_view.set_timer(500, self._show_number)  # wait a while and then display first number
        self._cs_event_system.add_callback("action", self._action)

    # -- in a loop --
    def _show_number(self):
        self._reset_stopwatch()
        self._cs_view.set_content("number", self._current_number)
        self._cs_view.set_timer(313, self._show_mask)

    def _show_mask(self):
        self._cs_view.set_content("mask")
        self._cs_view.set_timer(125, self._show_response_cue)

    def _show_response_cue(self):
        self._cs_view.set_content("response")
        self._cs_view.set_timer(63, self._show_after_mask)

    def _show_after_mask(self):
        self._cs_view.set_content("mask")
        self._cs_view.set_timer(375, self._show_fixation)

    def _show_fixation(self):
        self._cs_view.set_content("fixation")
        self._cs_view.set_timer(563, self._decide_test_end)

    # decide whether to continue looping or show result screen
    def _decide_test_end(self):
        # todo if action was not taken in this step, also write it down into data
        self._current_step += 1
        if self._tutorial_test and self._current_step == self._tutorial_step_count:
            self._show_tutorial_results()
        elif self._current_step == self._step_count:
            self._show_outro()
        else:
            self._current_number += 1
            if self._current_number == 10:
                self._current_number = 1
            self._show_number()
    # -- loop end --

    # --- INPUT EVALUATION ---
    def _action(self):
        action_time = self._get_stopwatch_time()
        self._current_cs_data.save_reaction(self._current_step, action_time)
        # debug
        if self._current_number == 3:
            print("[app] WRONG after", action_time, "s")
        else:
            print("[app] CORRECT after", action_time, "s")

    # --- OUTRO ---
    def _show_outro(self):
        self._current_cs_data.print_reactions()  # debug
        self._current_cs_data.evaluate_results()
        self._current_cs_data.print_results()  # debug
        self._current_cs_data.save_to_file()
        self._cs_event_system.remove_all_callbacks()
        self._cs_event_system.add_onetime_callback("action", self._show_results)
        self._cs_event_system.add_onetime_callback("action_alt", self._show_intro)
        self._cs_event_system.add_onetime_callback("back", self._cs_view.close)
        self._cs_view.set_content("outro")

    def _show_results(self):
        self._cs_event_system.add_onetime_callback("action_alt", self._show_intro)
        self._cs_event_system.add_onetime_callback("back", self._cs_view.close)
        self._cs_view.set_content("results", self._current_cs_data)

    # || Helper functions ||

    # start the stopwatch
    def _reset_stopwatch(self):
        # type: (CSPresenter) -> None
        self._stopwatch_start_time = time.clock()  # in python 3, the preffered call would be time.perf_counter()

    # stop stopwatch stopwatch and get time
    def _get_stopwatch_time(self):
        # type: (CSPresenter) -> float
        return time.clock() - self._stopwatch_start_time

