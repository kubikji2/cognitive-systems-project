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
    def __init__(self, cs_view, cs_event_system, cs_data):
        # type: (CSView, CSEventSystem, CSData) -> None

        print("[app] yay presenter instantiated")
        self._cs_view = cs_view
        self._cs_event_system = cs_event_system
        self._cs_data = cs_data

        # SART config
        self._step_count = 18  # type: int

        # state holders
        self._current_step = 0  # type: int
        self._current_number = 0  # type: int
        self._stopwatch_start_time = 0  # type: float  # used as a store for measuring time of user input

    # || The following functions each control a certain logical part/functionality of the app ||

    # --- INTRO ---
    # public
    # Sets up the app and shows it to user
    def start(self):
        self._cs_event_system.remove_all_callbacks()
        self._cs_event_system.add_onetime_callback("action", self._start_test)
        self._cs_event_system.add_onetime_callback("back", self._cs_view.close)
        self._cs_view.set_content("intro")
        # self._cs_view.warp_time(2)  # DEBUGGING SETTINGS
        self._cs_view.run()

    def _show_instructions(self):
        # todo
        pass

    def _start_tutorial(self):
        # todo?
        pass

    # --- TEST SEQUENCE ---
    # wait a while and then display first number
    def _start_test(self):
        self._cs_event_system.remove_all_callbacks()
        self._current_step = 0
        self._current_number = 1
        self._cs_data.init_test_data(self._step_count)
        self._cs_view.clear_content()
        self._cs_view.set_timer(225, self._show_number)

    # -- in a loop --
    def _show_number(self):
        self._cs_view.set_content("number", self._current_number)
        self._reset_stopwatch()
        self._cs_event_system.add_onetime_callback("action", self._action)
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
        if self._current_step == self._step_count:
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
        self._cs_data.save_reaction(self._current_step, action_time)
        if self._current_number == 3:
            print("[app] WRONG after " + str(action_time) + "s")
        else:
            print("[app] CORRECT after " + str(action_time) + "s")

    # --- OUTRO ---
    def _show_outro(self):
        self._cs_event_system.remove_all_callbacks()
        self._cs_event_system.add_onetime_callback("action", self._show_results)
        self._cs_data.print_reactions()
        self._cs_view.set_content("outro")

    def _show_results(self):
        # todo process collected data
        self._cs_data.save_to_file()
        self._cs_event_system.add_onetime_callback("action_alt", self.start)
        self._cs_event_system.add_onetime_callback("back", self._cs_view.close)
        self._cs_view.set_content("results")

    # || Helper functions ||

    # start the stopwatch
    def _reset_stopwatch(self):
        # type: (CSPresenter) -> None
        self._stopwatch_start_time = time.clock()  # in python 3, the preffered call would be time.perf_counter()

    # stop stopwatch stopwatch and get time
    def _get_stopwatch_time(self):
        # type: (CSPresenter) -> float
        return time.clock() - self._stopwatch_start_time

