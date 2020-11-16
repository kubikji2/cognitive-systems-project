#!/usr/bin/python2

import random as rnd
from typing import Optional

from CSVCImage import CSVCImage
from CSView import CSView
from CSEventSystem import CSEventSystem
from CSData import CSData
from CSViewContent import CSViewContent
from CSVCBase import CSVCBase
from CSVCIntro import CSVCIntro
from CSVCNumber import CSVCNumber
from CSVCResults import CSVCResults

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

        print("yay test instantiated")
        self._cs_view = cs_view
        self._cs_event_system = cs_event_system
        self._cs_data = cs_data

        # SART config
        self._step_count = 10  # type: int

        # state holders
        self._current_step = 0  # type: int
        self._current_number = 0  # type: int

    # || The following functions each control a certain logical part/functionality of the app ||

    # --- INTRO ---
    # public
    # Starts the whole test
    def start(self):
        self._cs_view.set_content(CSVCIntro(self._cs_view))
        self._cs_view.set_base_input_content(CSVCBase(self._cs_view))
        # self._cs_view.warp_time(2)
        self._cs_event_system.add_onetime_callback("action", self._start_test)
        self._cs_event_system.add_onetime_callback("back", self._cs_view.close)
        self._cs_view.run()

    def _show_instructions(self):
        # todo
        pass

    def _start_tutorial(self):
        # todo
        pass

    # --- TEST ---
    def _start_test(self):
        self._cs_event_system.remove_all_callbacks()
        self._current_step = 1
        self._cs_view.clear_content()
        self._cs_view.set_timer(225, self._show_number)

    def _show_number(self):
        self._current_number = rnd.randrange(0, 10)
        self._cs_view.set_content(CSVCNumber(self._cs_view, self._current_number))
        self._cs_view.set_timer(313, self._show_mask)

    def _show_mask(self):
        self._cs_event_system.add_onetime_callback("action", self._action)
        self._cs_view.set_content(CSVCImage(self._cs_view, "mask.png"))
        self._cs_view.set_timer(125, self._show_response)

    def _show_response(self):
        self._cs_view.set_content(CSVCImage(self._cs_view, "response.png"))
        self._cs_view.set_timer(63, self._show_after_mask)

    def _show_after_mask(self):
        self._cs_view.set_content(CSVCImage(self._cs_view, "mask.png"))
        self._cs_view.set_timer(375, self._show_fixation)

    def _show_fixation(self):
        self._cs_event_system.remove_onetime_callback("action")
        self._cs_view.set_content(CSVCImage(self._cs_view, "fixation.png"))
        self._cs_view.set_timer(563, self._blink)

    def _blink(self):
        self._cs_view.clear_content()
        if self._current_step == self._step_count:
            self._cs_view.set_timer(20, self._show_results)
        else:
            self._current_step += 1
            self._cs_view.set_timer(20, self._show_number)


    def _action(self):
        if self._current_number == 3:
            print("[app] ----------- WRONG PRESS!")
        else:
            print("[app] ----------- CORRECT PRESS!")

    # --- RESULTS ---
    def _show_results(self):
        self._cs_event_system.remove_all_callbacks()
        self._cs_event_system.add_callback("back", self._save_n_close)
        self._cs_event_system.add_callback("action_alt", self._start_test)
        self._cs_view.set_content(CSVCResults(self._cs_view))

    def _save_n_close(self):
        self._cs_data.save_to_file()
        self._cs_view.close()
