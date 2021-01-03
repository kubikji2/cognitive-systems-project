import random as rnd
import sys
import time
# from threading import Thread
from typing import Optional, List

from CSView import CSView
from CSEventSystem import CSEventSystem
from CSData import CSData
import CSDataSaver

# for browsing files
import glob

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
        self._step_count = 243  # type: int
        self._tutorial_step_count = 27  # type: int

        # state holders
        self._current_cs_data = None  # type: Optional[CSData]  # the CSData object for storing reactions during the test and viewing results after the test
        self._loaded_cs_data = []  # type: List[CSData]  # all CSData objects loaded from files for browsing results
        self._csd_index = -1  # type: int  # index of currently shown CSData object while browsing results
        self._is_result_halved = False  # type: bool  # used to indicate whether result is shown overally for the whole test or as a comparison of the two halves of the test
        self._username = ""  # type: str
        self._is_tutorial = True  # type: bool
        self._current_step = 0  # type: int
        self._current_number = 0  # type: int
        self._stopwatch_start_time = 0  # type: float  # used as a store for measuring time of user input

        # setup the most precise timer for Python 2.7
        # in python 3, the preffered call would be time.perf_counter()
        # https://www.pythoncentral.io/measure-time-in-python-time-time-vs-time-clock/
        # https://www.tutorialspoint.com/python/time_clock.htm
        # https://docs.microsoft.com/en-us/windows/win32/api/profileapi/nf-profileapi-queryperformancecounter
        if sys.platform == 'win32':
            # On Windows, the best timer is time.clock (most precise of em all)
            self._stopwatch_time = time.clock
        else:
            # On most other platforms the best timer is time.time (time.clock returns CPU time which is wrong)
            self._stopwatch_time = time.time

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
        self._csd_index = -1
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
        self._cs_event_system.remove_all_callbacks()
        # load all cs_data files
        filenames = glob.glob("Results/*" + CSDataSaver.CSData_FILE_SUFFIX)  # todo move this to csdatasaver (it could be better if it was static)
        print("[CSPresenter] files found: " + str(filenames))
        self._loaded_cs_data = []
        for filename in filenames:
            cs_data = CSData(filename=filename)
            self._loaded_cs_data.append(cs_data)
        if not self._loaded_cs_data:
            print("[CSPresenter] No results to display")
            self._cs_event_system.add_onetime_callback("action_alt", self._show_saved_results)
            self._cs_event_system.add_onetime_callback("back", self._show_intro)
            self._cs_view.set_content("results", (None, None, None, None))
        else:
            self._csd_index = 0
            # self._current_cs_data = self._loaded_cs_data[self._csd_index]
            self._is_result_halved = False
            self._cs_event_system.add_onetime_callback("back", self._show_intro)
            self._cs_event_system.add_callback("action", self._switch_halved)
            # self._cs_event_system.add_callback("action_alt", self._debug_eval_and_show)
            self._cs_event_system.add_callback("left", self._previous_result)
            self._cs_event_system.add_callback("right", self._next_result)
            self._show_result()

    # def _debug_eval_and_show(self):
    #     self._loaded_cs_data[self._csd_index].evaluate_results()
    #     self._show_result()

    def _switch_halved(self):
        self._is_result_halved = not self._is_result_halved
        self._show_result()

    def _next_result(self):
        self._csd_index += 1
        if self._csd_index == len(self._loaded_cs_data):
            self._csd_index = 0
        self._show_result()

    def _previous_result(self):
        self._csd_index -= 1
        if self._csd_index == -1:
            self._csd_index = len(self._loaded_cs_data) - 1
        self._show_result()

    def _show_result(self):
        # self._loaded_cs_data[self._csd_index].evaluate_results()  # debug
        self._loaded_cs_data[self._csd_index].print_results()  # debug
        # self._loaded_cs_data[self._csd_index].save_to_file()  # debug
        self._cs_view.set_content("results", (self._loaded_cs_data[self._csd_index], self._is_result_halved, self._csd_index + 1, len(self._loaded_cs_data)))

    # --- TEST SEQUENCE ---
    def _start_tutorial(self):
        self._cs_event_system.remove_all_callbacks()
        self._is_tutorial = True
        self._current_step = 0
        self._current_number = 1
        self._current_cs_data = CSData(step_count=self._tutorial_step_count, name=self._username)
        self._show_ready()

    def _start_test(self):
        self._cs_event_system.remove_all_callbacks()
        self._is_tutorial = False
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
        self._cs_event_system.add_callback("any", self._reaction)

    # -- in a loop --
    def _show_number(self):
        self._start_stopwatch()
        self._cs_view.set_timer(313, self._show_mask)
        self._cs_view.set_timer(438, self._show_response_cue)
        self._cs_view.set_timer(501, self._show_after_mask)
        self._cs_view.set_timer(876, self._show_fixation)
        self._cs_view.set_timer(1439, self._decide_test_end)
        self._cs_view.set_content("number", self._current_number)

    def _show_mask(self):
        self._cs_view.set_content("mask")

    def _show_response_cue(self):
        self._cs_view.set_content("response")

    def _show_after_mask(self):
        self._cs_view.set_content("mask")

    def _show_fixation(self):
        self._cs_view.set_content("fixation")

    # decide whether to continue looping or show result screen
    def _decide_test_end(self):
        self._current_step += 1
        if self._is_tutorial and self._current_step == self._tutorial_step_count:
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
    def _reaction(self):
        action_time = self._get_stopwatch_time()
        self._current_cs_data.save_reaction(self._current_step, action_time)
        # debug
        if self._current_number == 3:
            # print("[app] WRONG after", action_time, "s")
            pass
        else:
            # print("[app] CORRECT after", action_time, "s")
            pass

    # --- OUTRO ---
    def _show_outro(self):
        self._cs_event_system.remove_all_callbacks()
        self._current_cs_data.print_reactions()  # debug
        self._current_cs_data.evaluate_results()
        self._current_cs_data.print_results()  # debug
        self._current_cs_data.save_to_file()
        self._cs_event_system.add_onetime_callback("action", self._show_test_result)
        self._cs_event_system.add_onetime_callback("action_alt", self._show_intro)
        self._cs_event_system.add_onetime_callback("back", self._cs_view.close)
        self._cs_view.set_content("outro")

    def _show_test_result(self):
        self._cs_event_system.remove_all_callbacks()
        self._is_result_halved = False
        self._cs_event_system.add_callback("action", self._switch_test_result_halved)
        self._cs_event_system.add_onetime_callback("action_alt", self._show_intro)
        self._cs_event_system.add_onetime_callback("back", self._cs_view.close)
        self._cs_view.set_content("results", (self._current_cs_data, self._is_result_halved, None, None))

    def _switch_test_result_halved(self):
        self._is_result_halved = not self._is_result_halved
        self._cs_view.set_content("results", (self._current_cs_data, self._is_result_halved, None, None))

    # || Helper functions ||

    # start the stopwatch
    def _start_stopwatch(self):
        # type: (CSPresenter) -> None
        self._stopwatch_start_time = self._stopwatch_time()

    # stop stopwatch stopwatch and get time
    def _get_stopwatch_time(self):
        # type: (CSPresenter) -> float
        return self._stopwatch_time() - self._stopwatch_start_time

