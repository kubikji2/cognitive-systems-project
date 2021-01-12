from scipy.interpolate import interp1d
from typing import List, Tuple
import numpy as np
from scipy import fftpack
import datetime

# saves CSData to keep this file clean
import CSDataSaver

WHOLE = 0
FIRST = 1
SECOND = 2
PARTS = [WHOLE, FIRST, SECOND]

DIGITS_EXCEPT_3 = [4, 5, 6, 7, 8, 9, 1, 2]

TOO_EARLY_TIME = 150.0
STEP_TIME = 1439.0

"""
A class for storing and processing test data
"""
class CSData:
    # (data type specifications for better debugging)

    # test info
    step_count = None  # type: List[int]
    name = None  # type: str # todo
    timestamp = None  # type

    # list for reaction collection and multiple press error counter
    _seconds = []  # type: List[float]  # saved user input times in seconds per step (0 if no key pressed)
    _multiple_press_errors = None  # type: List[int]

    # resulting stats: [0] whole [1] first half [2] second half
    ms = None  # type: List[List[float]]
    ms_stripped = None  # type: List[List[float]]
    step_nums_stripped = None  # type: List[List[int]]
    ms_interpolated = None  # type: List[List[float]]
    mean_by_digit = None  # type: List[List[float]]
    fft = None  # type: List[List[float]]
    fft_freq = None  # type: List[List[float]]
    aus = None  # type: List[float]
    mean = None  # type: List[float]
    std_dev = None  # type: List[float]
    regression_line = None  # type: Tuple[float, float]
    comission_errors = None  # type: List[int]
    omission_errors = None  # type: List[int]
    other_errors = None  # type: List[int]

    # CSData can either be instantiated as:
    # a new data instance by passing step_count and name
    # or
    # loaded from an exisisting file by passing filename

    def __init__(self, step_count=None, name=None, filename=None):
        # type: (int, str, str) -> None

        if step_count is not None and name is not None:
            self.step_count = [[], [], []]
            self.step_count[WHOLE] = step_count
            # calculate how many steps will be in each half of the test
            bigger_half = (self.step_count[WHOLE] + 1) // 2  # bigger half if odd number of steps
            self.step_count[FIRST] = bigger_half
            self.step_count[SECOND] = self.step_count[WHOLE] - bigger_half
            self.name = name
            self.timestamp = datetime.datetime.now()  # save creation time
            # allocate list for reaction collection and init multiple press error counter
            self._seconds = [0.0] * step_count
            self._multiple_press_errors = [0, 0, 0]
            # init dummy results
            self.ms = [[], [], []]  # times in ms
            self.ms_stripped = [[], [], []]  # only correct presses for means and slope
            self.step_nums_stripped = [[], [], []]  # specifies the step numbers of the corresponding stripped times
            self.ms_interpolated = [[], [], []]  # for FFT analysis
            self.mean_by_digit = [[], [], []]  # means for digits 4, 5, 6, 7, 8, 9, 1, 2
            self.fft = [[], [], []]  # resulting amplitudes/powers of frequencies from FFT
            self.fft_freq = [[], [], []]  # corresponding frequencies from FFT
            self.aus = [0.0, 0.0, 0.0]  # area under spectrum from FFT
            self.mean = [0.0, 0.0, 0.0]
            self.std_dev = [0.0, 0.0, 0.0]
            self.regression_line = (0.0, 0.0)  # [0] is the y offset, [1] is the slope
            self.comission_errors = [0, 0, 0]  # presses on target trials
            self.omission_errors = [0, 0, 0]  # missed presses on non-target trials
            self.other_errors = [0, 0, 0]  # presses out of regular time window or multiple presses per step

        elif filename is not None:
            self.load_from_file(filename)
            
        else:
            print("[CSData] ERROR - please specify either step_count and name or filename when creating this object")

    # --- interface for PRESENTER ---

    # saves the time for a specified step into the data list
    def save_reaction(self, step, time):
        # type: (int, float) -> None

        if self._seconds[step] == 0.0:  # time not yet stored for this step
            self._seconds[step] = time
        else:                           # time already stored for this step
            self._multiple_press_errors[WHOLE] += 1
            if step < self.step_count[FIRST]:
                self._multiple_press_errors[FIRST] += 1
            else:
                self._multiple_press_errors[SECOND] += 1

    # debug function to print collected times
    def print_reactions(self):
        print(self._seconds)

    # command to calculate additional information from the currently collected times
    def evaluate_results(self):
        self._prepare_data_lists_and_calculate_mean_by_digit()
        self._calculate_mean()
        self._calculate_std_dev()
        self._do_linear_regression()
        self._calculate_fft()

    # debug function to print calculated results
    def print_results(self):
        print("Reaction times:")
        print(self.ms[WHOLE])
        print(self.ms[FIRST]),
        print(self.ms[SECOND])
        print()
        print("Interpolated times:")
        print(self.ms_interpolated[WHOLE])
        print(self.ms_interpolated[FIRST]),
        print(self.ms_interpolated[SECOND])
        print()
        print("Step counts:", self.step_count[WHOLE], self.step_count[FIRST], self.step_count[SECOND])
        print("Comission errors:", self.comission_errors[WHOLE], self.comission_errors[FIRST], self.comission_errors[SECOND])
        print("Omission errors:", self.omission_errors[WHOLE], self.omission_errors[FIRST], self.omission_errors[SECOND])
        print("Other errors:", self.other_errors[WHOLE], self.other_errors[FIRST], self.other_errors[SECOND])
        print()
        print("Stripped times:")
        print(zip(self.step_nums_stripped[WHOLE], self.ms_stripped[WHOLE]))
        print(zip(self.step_nums_stripped[FIRST], self.ms_stripped[FIRST])),
        print(zip(self.step_nums_stripped[FIRST], self.ms_stripped[SECOND]))
        print()
        print("Means by digits: ")
        print(zip(DIGITS_EXCEPT_3, self.mean_by_digit[WHOLE]))
        print(zip(DIGITS_EXCEPT_3, self.mean_by_digit[FIRST])),
        print(zip(DIGITS_EXCEPT_3, self.mean_by_digit[SECOND]))
        print()
        print("FFT: ")
        print(self.fft[WHOLE])
        print(self.fft_freq[WHOLE])
        print(self.fft[FIRST]),
        print(self.fft[SECOND])
        print(self.fft_freq[FIRST]),
        print(self.fft_freq[SECOND])
        print()
        print("AUS:", self.aus[WHOLE], self.aus[FIRST], self.aus[SECOND])
        print("Means:", self.mean[WHOLE], self.mean[FIRST], self.mean[SECOND])
        print("Std devs:", self.std_dev[WHOLE], self.std_dev[FIRST], self.std_dev[SECOND])
        print("Regression line:", self.regression_line[0], self.regression_line[1])

    # saves current state of data to file
    def save_to_file(self):
        csd = CSDataSaver.CSDataSaver(self)
        csd.save_data()
        print("[CSData] data file created")

    def load_from_file(self, filename):
        csd = CSDataSaver.CSDataSaver(self)
        csd.load_data(filename)
        print("[CSData] data loaded from file")

    # --- private methods ---

    def _prepare_data_lists_and_calculate_mean_by_digit(self):
        # convert seconds to ms
        self.ms[WHOLE] = [1000.0 * x for x in self._seconds]
        # divide in two halves
        self.ms[FIRST] = self.ms[WHOLE][:self.step_count[FIRST]]
        self.ms[SECOND] = self.ms[WHOLE][self.step_count[FIRST]:]
        # prepare list for means by digits
        self.mean_by_digit = [[0.0 for digit in range(len(DIGITS_EXCEPT_3))] for part in PARTS]
        step_count_per_digit = [[0 for digit in range(len(DIGITS_EXCEPT_3))] for part in PARTS]  # type: List[List[int]]

        # fill in various lists for data evaluation
        for step in range(0, self.step_count[WHOLE]):
            time = self.ms[WHOLE][step]
            part = FIRST if (step < self.step_count[FIRST]) else SECOND

            # catch times too early/late after number was shown
            if time != 0.0 and not self._is_time_acceptable(time):
                self.other_errors[WHOLE] += 1
                self.other_errors[part] += 1
                continue

            # on digit 3
            if self._digit_from_step(step) == 3:
                if time != 0:  # pressed
                    self.comission_errors[WHOLE] += 1
                    self.comission_errors[part] += 1
                    # note: zvazit zapocteni casu do stripped / interpolated listu DONE -> nope

                else:  # missed
                    pass

            # on digits 1,2,4,5,6,7,8,9
            else:
                if time != 0:  # pressed
                    self.ms_stripped[WHOLE].append(time)
                    self.ms_stripped[part].append(time)
                    self.step_nums_stripped[WHOLE].append(step)
                    self.step_nums_stripped[part].append(step)
                    index_of_digit = self._index_from_digit(self._digit_from_step(step))
                    self.mean_by_digit[WHOLE][index_of_digit] += time
                    self.mean_by_digit[part][index_of_digit] += time
                    step_count_per_digit[WHOLE][index_of_digit] += 1
                    step_count_per_digit[part][index_of_digit] += 1

                else:  # missed
                    self.omission_errors[WHOLE] += 1
                    self.omission_errors[part] += 1

        # finish calculating mean by digit
        for part in PARTS:
            for index_of_digit in range(len(DIGITS_EXCEPT_3)):
                if step_count_per_digit[part][index_of_digit] != 0:
                    self.mean_by_digit[part][index_of_digit] /= float(step_count_per_digit[part][index_of_digit])

        # add multiple press errors to other errors
        for part in PARTS:
            self.other_errors[part] += self._multiple_press_errors[part]

        # make interpolated lists for FFT
        self._create_interpolated_lists()

    def _digit_from_step(self, step_num):
        return (step_num % 9) + 1

    def _index_from_digit(self, digit):
        return DIGITS_EXCEPT_3.index(digit)

    def _create_interpolated_lists(self):
        # initialize the whole list to values in ms
        self.ms_interpolated[WHOLE] = [x for x in self.ms[WHOLE]]

        # fill beginning of the list with the first acceptable time
        index_of_first_acceptable_time = next((i for i, time in enumerate(self.ms_interpolated[WHOLE]) if self._is_time_acceptable(time)), None)
        for i in range(index_of_first_acceptable_time):
            self.ms_interpolated[WHOLE][i] = self.ms_interpolated[WHOLE][index_of_first_acceptable_time]

        # fill ending of the list with the last acceptable time
        index_of_last_acceptable_time = 0
        for i, time in enumerate(reversed(self.ms_interpolated[WHOLE])):
            if self._is_time_acceptable(time):
                index_of_last_acceptable_time = len(self.ms_interpolated[WHOLE]) - i - 1
                break
        for i in range(len(self.ms_interpolated[WHOLE]) - 1, index_of_last_acceptable_time, -1):
            self.ms_interpolated[WHOLE][i] = self.ms_interpolated[WHOLE][index_of_last_acceptable_time]

        # we have [y], generate evenly spaced linspace [x], generate list of indexes with acceptable numbers [idx], create interpolation function from y between them [f_interpolation], call it on the linspace to get our [ynew]
        # https://stackoverflow.com/questions/45794490/replace-zeros-in-numpy-array-with-linear-interpolation-between-its-preceding-and
        y = np.array(self.ms_interpolated[WHOLE])
        x = np.arange(len(y))
        # making a single condition like >, =, or < on a np.array with a number returns a np.array of booleans, and np.where with this condition without specified x and y returns non-zero (True) indicies of that array -> our [idx]
        # since i need to have a ternary operation as in _is_time_acceptable i use vectorize to help me and use np.nonzero instead
        # https://stackoverflow.com/questions/39109045/numpy-where-with-multiple-conditions
        f_acceptable = np.vectorize(self._is_time_acceptable)
        idx_bools = f_acceptable(y)
        idx = np.nonzero(idx_bools)
        f_interpolation = interp1d(x[idx], y[idx])
        ynew = f_interpolation(x)
        self.ms_interpolated[WHOLE] = ynew.tolist()

        # copy results to halved lists
        self.ms_interpolated[FIRST] = self.ms_interpolated[WHOLE][:self.step_count[FIRST]]
        self.ms_interpolated[SECOND] = self.ms_interpolated[WHOLE][self.step_count[FIRST]:]

    def _is_time_acceptable(self, time):
        return TOO_EARLY_TIME < time < STEP_TIME

    def _calculate_mean(self):
        for part in PARTS:
            if self.ms_stripped[part]:
                self.mean[part] = sum(self.ms_stripped[part]) / len(self.ms_stripped[part])
            else:
                self.mean[part] = 0.0

    def _calculate_std_dev(self):
        square_deviations = [[], [], []]  # type: List[List[float]]
        variance = [0.0, 0.0, 0.0]  # type: List[float]
        for part in PARTS:
            if self.ms_stripped[part]:
                square_deviations[part] = [(x - self.mean[part]) ** 2.0 for x in self.ms_stripped[part]]
                variance[part] = sum(square_deviations[part]) / float(len(square_deviations[part]))
                self.std_dev[part] = np.sqrt(variance[part])
            else:
                self.std_dev[part] = 0.0

    def _calculate_fft(self):
        # reference for scipy FFT https://www.youtube.com/watch?v=b06pFMIRO0I
        # fastness of computation https://dsp.stackexchange.com/questions/10933/fourier-transform-to-the-power-of-two
        # (using dirrectly matplotlibs PSD https://matplotlib.org/3.3.3/gallery/lines_bars_and_markers/psd_demo.html#sphx-glr-gallery-lines-bars-and-markers-psd-demo-py)
        # how to get PSD otherwise https://www.researchgate.net/post/What-formula-should-I-use-to-calculate-the-power-spectrum-density-of-a-FFT
        # also fft to psd https://www.mathworks.com/help/signal/ug/power-spectral-density-estimates-using-fft.html
        # bin width https://stackoverflow.com/questions/10754549/fft-bin-width-clarification

        for part in PARTS:
            # check
            assert(self.step_count[part] == len(self.ms_interpolated[part]))

            # EDIT --- additional data preparation (removal of constant and linear component, since they're already being analyzed before) ---
            # [linear regression copied]
            x = np.arange(0, self.step_count[part])
            y = np.array(self.ms_interpolated[part])

            # number of observations/points
            n = np.size(x)

            # mean of x and y vector
            m_x, m_y = np.mean(x), np.mean(y)

            # calculating cross-deviation and deviation about x
            ss_xy = np.sum(y * x) - n * m_y * m_x
            ss_xx = np.sum(x * x) - n * m_x * m_x

            # calculating regression coefficients
            b_1 = ss_xy / ss_xx
            b_0 = m_y - b_1 * m_x

            lin_line = b_1 * x
            new_y = y - b_0 - lin_line
            # ---

            # https://stackoverflow.com/questions/62106028/what-is-the-difference-between-np-linspace-and-np-arange
            # https://stackoverflow.com/questions/31820107/is-there-a-numpy-function-that-allows-you-to-specify-start-step-and-number
            # time_vector = np.linspace(0, self.step_count[part]) * STEP_TIME / 1000.0 # we dont need it

            # useful variables
            bin_width = STEP_TIME / 1000.0  # IMPORTANT even if we have the values in ms, we want the x axis (frequencies) in Hz aka 1/s
            sampling_frequency = 1 / bin_width  # in Hz, should be 1 / 1.439 = 0.6949 Hz
            n_samples = self.step_count[part]
            signal = new_y  # --- EDIT from np.array(self.ms_interpolated[part])
            frequencies = fftpack.fftfreq(n_samples, bin_width)  # here we use step time in seconds so we can have frequencies in Hz (1/s) instead of 1/ms

            # calculation
            signal_fft = fftpack.fft(signal)  # calculating FFT -> array with complex number results of FFT
            assert(signal_fft.size == n_samples)
            amplitudes = np.abs(signal_fft)  # by making absolute values -> array of amplitudes of frequencies
            amplitudes_scaled = amplitudes / n_samples
            # divided by the num of samples so that the amps are samely scaled for different n_samples
            # at amplitudes_scaled[0] we can find the mean value (this is slightly different to regular mean due to interpolation)
            # powers = amplitudes**2  # weirdly high
            # power_spectral_density = powers * bin_width / n_samples   # PSD(fk) = |X(fk)|^2 / (Fsampling * Nsamples) = |X(fk)|^2 * bin_width / Nsamples
            # intuitively, think about it with the area under spectrum in mind, each sample is a column of certain width

            # writing to data
            self.fft[part] = amplitudes_scaled.tolist()[1: n_samples//2 + 1]
            self.fft_freq[part] = frequencies.tolist()[1: n_samples//2 + 1]  # [0, 0.1, 0.2, -0.3, -0.2, -0.1] -> [0.1, 0.2, -0.3]
            if n_samples % 2 == 0:
                self.fft_freq[part][-1] *= -1.0  # convert the last negative freq to positive (its the nyquist / hlaf the sampling freq)
            self.aus[part] = sum(self.fft[part]) / n_samples  # its my own AUS - sum ~ integral, and since amp_scaled are normalized, then only thing remaining after sum is divide once more by n_samples, and this should be a normalized value across varying n_samples

            debug = False
            if debug:
                np.set_printoptions(precision=3, suppress=True, linewidth=np.inf)
                print("mean: {}".format(np.mean(self.ms_interpolated[part])))
                print("bin width: {}".format(bin_width))
                print("sampling frq: {}".format(sampling_frequency))
                print("n_samples: {}".format(n_samples))
                print("interpolated: {}".format(self.ms_interpolated[part]))
                print("inter. scal.: {}".format(new_y))
                print("mean inter. scal.: {}".format(np.mean(new_y)))
                print("amplitudes: {}".format(amplitudes))
                print("amplitudes scaled: {}".format(amplitudes_scaled))
                # print("powers: {}".format(powers))
                # print("PSD: {}".format(power_spectral_density))
                print("frequencies: {}".format(frequencies))
                print("frequencies_ {}".format(self.fft_freq[part]))



    # taken from https://www.geeksforgeeks.org/linear-regression-python-implementation/
    def _do_linear_regression(self):
        x = np.array(self.step_nums_stripped[WHOLE])
        y = np.array(self.ms_stripped[WHOLE])

        # number of observations/points
        n = np.size(x)

        # mean of x and y vector
        m_x, m_y = np.mean(x), np.mean(y)

        # calculating cross-deviation and deviation about x
        ss_xy = np.sum(y * x) - n * m_y * m_x
        ss_xx = np.sum(x * x) - n * m_x * m_x

        # calculating regression coefficients
        b_1 = ss_xy / ss_xx
        b_0 = m_y - b_1 * m_x

        self.regression_line = (b_0, b_1)

    # --- property-like interface for VIEW --- EDIT: removed and instead made the key stuffs public

    def get_total_errors(self):
        # return [x + y + z for x, y, z in zip(self.comission_errors, self.omission_errors, self.other_errors)]
        return [x + y for x, y in zip(self.comission_errors, self.omission_errors)]
