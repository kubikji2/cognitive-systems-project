#!/usr/bin/python2

"""
A class for storing and processing test data
"""
class CSData:
    def __init__(self):
        self._step_count = 0
        self._reaction_times = []  # if the user pressed the key, how long fif it take? (0 for no key pressed)

    def init_test_data(self, step_count):
        # type: (int) -> None
        self._reaction_times = [0] * step_count

    def save_reaction(self, step, time):
        # type: (int, float) -> None
        self._reaction_times[step] = time


    def save_to_file(self):
        # TODO
        pass

    def print_reactions(self):
        print(self._reaction_times)

    def evaluate_results(self):
        self._evaluate_mean()

    def _pick_usable_data(self):
        pass

    def _evaluate_mean(self):

        pass

    def _evaluate_fft(self):
        # TODO
        pass
