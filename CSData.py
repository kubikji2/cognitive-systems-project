#!/usr/bin/python2

"""
A class for storing and processing test data
"""
class CSData:
    def __init__(self):
        self._reaction_times = []  # if the user pressed the key, how long fif it take? (0 for no key pressed)

    def init_test_data(self, step_count):
        # type: (int) -> None
        self._reaction_times = [0] * step_count

    def save_reaction(self, step, time):
        # type: (int, float) -> None
        self._reaction_times[step] = time

    def evaluate_fft(self):
        # TODO
        pass

    def save_to_file(self):
        # TODO
        pass

    def print_reactions(self):
        print(self._reaction_times)
