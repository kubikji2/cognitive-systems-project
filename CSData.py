#!/usr/bin/python2

from typing import List
import math

WHOLE = 0
FIRST = 1
SECOND = 2

"""
A class for storing and processing test data
"""
class CSData:
    # data type specifications for better debugging
    _step_count = None  # type: List[int]
    _ms = None  # type: List[List[float]]
    _ms_stripped = None  # type: List[List[float]]
    _ms_interpolated = None  # type: List[List[float]]
    _ms_by_number = None  # type: List[List[float]]
    _mean = None  # type: List[float]
    _std_dev = None  # type: List[float]
    _comission_errors = None  # type: List[int]
    _omission_errors = None  # type: List[int]
    _random_errors = None  # type: List[int]

    def __init__(self):
        # collected list
        self._seconds = []  # type: List[float] # saved user input times in seconds per step (0 if no key pressed)

        # resulting stats: [0] whole [1] first half [2] second half
        self._ms = [[], [], []]  # times in ms
        self._ms_stripped = [[], [], []]  # only correct presses for means and slope
        self._ms_interpolated = [[], [], []]  # for FFT analysis
        self._step_count = [0, 0, 0]
        self._mean = [0, 0, 0]
        self._std_dev = [0, 0, 0]
        self._comission_errors = [0, 0, 0]  # presses on target trials
        self._omission_errors = [0, 0, 0]  # missed presses on non-target trials
        self._random_errors = [0, 0, 0]  # presses out of regular time window or multiple presses per step

    # --- interface for PRESENTER ---

    # must be called before you call save_reaction for the first time, inits the data list with zeros for given length
    def init_test_data(self, step_count):
        # type: (int) -> None
        # init data
        self.__init__()
        self._step_count[WHOLE] = step_count
        self._seconds = [0] * step_count

        # calculate how many steps will be in each half of the test
        bigger_half = (self._step_count[WHOLE] + 1) // 2  # bigger half if odd number of steps
        self._step_count[FIRST] = bigger_half
        self._step_count[SECOND] = self._step_count[WHOLE] - bigger_half

    # saves the time for a specified step into the data list
    def save_reaction(self, step, time):
        # type: (int, float) -> None

        if self._seconds[step] == 0.0:  # time not yet stored for this step
            self._seconds[step] = time
        else:                           # time already stored for this step
            self._random_errors[WHOLE] += 1
            if step < self._step_count[FIRST]:
                self._random_errors[FIRST] += 1
            else:
                self._random_errors[SECOND] += 1

    # debug function to print collected times
    def print_reactions(self):
        print(self._seconds)

    # command to calculate additional information from the currently collected times
    def evaluate_results(self):
        self._prepare_data()
        self._calculate_mean()
        self._calculate_std_dev()

    # debug function to print calculated results
    def print_results(self):
        print("Reaction times:")
        print(self._ms[WHOLE])
        print(self._ms[FIRST]),
        print(self._ms[SECOND])
        print()
        print("Step counts:", self._step_count[WHOLE], self._step_count[FIRST], self._step_count[SECOND])
        print("Comission errors:", self._comission_errors[WHOLE], self._comission_errors[FIRST], self._comission_errors[SECOND])
        print("Omission errors:", self._omission_errors[WHOLE], self._omission_errors[FIRST], self._omission_errors[SECOND])
        print("Random errors:", self._random_errors[WHOLE], self._random_errors[FIRST], self._random_errors[SECOND])
        print()
        print("Stripped times:")
        print(self._ms_stripped[WHOLE])
        print(self._ms_stripped[FIRST]),
        print(self._ms_stripped[SECOND])
        print()
        print("Means:", self._mean[WHOLE], self._mean[FIRST], self._mean[SECOND])
        print("Std devs:", self._std_dev[WHOLE], self._std_dev[FIRST], self._std_dev[SECOND])

    # saves current state of data to file
    def save_to_file(self):
        # TODO
        pass

    # --- private methods ---

    def _prepare_data(self):
        # convert seconds to ms
        self._ms[WHOLE] = [1000.0 * x for x in self._seconds]
        # divide in two halves
        self._ms[FIRST] = self._ms[WHOLE][:self._step_count[FIRST]]
        self._ms[SECOND] = self._ms[WHOLE][self._step_count[FIRST]:]

        # create stripped and [todo interpolated lists] with prettier data
        for i in range(0, self._step_count[WHOLE]):
            time = self._ms[WHOLE][i]
            part = FIRST if (i < self._step_count[FIRST]) else SECOND

            # catch times too early/late after number was shown
            if 0.0 < time < 150.0 or 1439.0 < time:
                self._random_errors[WHOLE] += 1
                self._random_errors[part] += 1
                continue

            # on digit 3
            if i % 9 == 2:
                if time != 0:  # pressed
                    self._comission_errors[WHOLE] += 1
                    self._comission_errors[part] += 1
                    # todo zvazit zapocteni casu do stripped / interpolated listu

                else:  # missed
                    pass

            # on digits 1,2,4,5,6,7,8,9
            else:
                if time != 0:  # pressed
                    self._ms_stripped[WHOLE].append(time)
                    self._ms_stripped[part].append(time)

                else:  # missed
                    self._omission_errors[WHOLE] += 1
                    self._omission_errors[part] += 1


    def _calculate_mean(self):
        for part in [WHOLE, FIRST, SECOND]:
            self._mean[part] = sum(self._ms_stripped[part]) / len(self._ms_stripped[part])

    def _calculate_std_dev(self):
        square_deviations = [[], [], []]  # type: List[List[float]]
        variance = [0.0, 0.0, 0.0]  # type: List[float]
        for part in [WHOLE, FIRST, SECOND]:
            square_deviations[part] = [(x - self._mean[part]) ** 2.0 for x in self._ms_stripped[part]]
            variance[part] = sum(square_deviations[part]) / float(len(square_deviations[part]))
            self._std_dev[part] = math.sqrt(variance[part])

    def _evaluate_fft(self):
        # TODO
        pass

    # --- property-like interface for VIEW ---

    def get_mean(self):
        return self._mean

    # TODO etc
