#!/usr/bin/python2

import Tkinter as Tk


from TkinterViewContent import TkinterViewContent
from CSData import *
from typing import Optional, Union

import matplotlib
from matplotlib.ticker import MultipleLocator
matplotlib.use("TkAgg")  # setting matplotlib to use the 'Tkinter Anti-grain renderer' backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt  # diference of pyplot and figure here: https://stackoverflow.com/questions/5450207/whats-the-difference-between-matplotlib-pyplot-and-matplotlib-figure

RT_TIME_MAX = 1000  # STEP_TIME
RT_TIME_MIN = 200  # TOO_EARLY_TIME + 100
DGM_TIME_MAX = 800
DGM_TIME_MIN = 300
FFT_TIME_MAX = 60
FREQ_MAX = 0.35
PSP_FREQ = 0.0772  # principle SART peak frequency (once per whole 1-9 cycle)
RESPONSE_CUE_START = 438
RESPONSE_CUE_END = 501

"""
Screen showing the results to the user. |WARNING| Please do not judge this class, could be done better in a million ways :D 
"""
class TVCResults(TkinterViewContent):

    def __init__(self):
        self._cs_data = None  # type: Optional[CSData]
        self._halved = None  # type: Optional[bool]
        self._index = None  # type: Optional[int]
        self._max_index = None  # type: Optional[int]

    def show(self, parent):
        # BROWSING PREVIOUSLY SAVED RESULTS BUT NONE FOUND
        if self._cs_data is None:
            err = Tk.Label(parent, text="No saved results found")
            err.grid(row=0)
            err1 = Tk.Label(parent, text="Press R to try again")
            err1.grid(row=1)
            err2 = Tk.Label(parent, text="Press Esc to go back")
            err2.grid(row=2)
            return

        # OVERALL RESULT
        if not self._halved:
            # SHOWING RESULT OF THE CURRENT TEST
            if self._index is None or self._max_index is None:
                # TOP
                lbl_header = Tk.Label(parent, text="Overall result", font=("Arial", 24))
                lbl_controls1 = Tk.Label(parent, text="Press Enter or space to switch to half-by-half comparison", font=("Arial", 14))
                lbl_controls2 = Tk.Label(parent, text="Press R to go back to intro")
                lbl_controls3 = Tk.Label(parent, text="Press Esc to exit")
            # BROWSING PREVIOUSLY SAVED RESULTS
            else:
                lbl_header = Tk.Label(parent, text="Overall result {} of {}".format(self._index, self._max_index), font=("Arial", 16))
                lbl_controls1 = Tk.Label(parent, text="Press Enter or space to switch to half-by-half comparison")
                lbl_controls2 = Tk.Label(parent, text="Press Left / Right to browse results")
                lbl_controls3 = Tk.Label(parent, text="Press Esc to go back to intro")
            lbl_sub_header = Tk.Label(parent, text=(self._cs_data.name + " " + str(self._cs_data.timestamp.strftime("%Y-%m-%d %H:%M:%S"))), font=("Arial", 14))

            frm_results = Tk.Frame(parent)

            frm_left = Tk.Frame(frm_results)
            frm_left.columnconfigure(0, weight=1, minsize=220)
            frm_left.columnconfigure(1, weight=1, minsize=70)

            frm_right = Tk.Frame(frm_results)
            frm_right.columnconfigure(0, weight=1, minsize=200)
            frm_right.columnconfigure(1, weight=1, minsize=200)
            frm_right.rowconfigure(0, weight=1, minsize=100)
            frm_right.rowconfigure(1, weight=1, minsize=100)

            #    LEFT
            lbl_trials = Tk.Label(frm_left, text="Total trials:", font=("Arial", 14))
            lbl_trials_ = Tk.Label(frm_left, text="{}".format(self._cs_data.step_count[WHOLE]), font=("Arial", 16))
            lbl_trials.grid(row=0, column=0, sticky='w', pady=(15, 0))
            lbl_trials_.grid(row=0, column=1, sticky='w', pady=(15, 0))
            lbl_com_err = Tk.Label(frm_left, text="Comission errors:", font=("Arial", 14))
            lbl_com_err_ = Tk.Label(frm_left, text="{}".format(self._cs_data.comission_errors[WHOLE]), font=("Arial", 16), fg='coral')
            lbl_com_err.grid(row=1, column=0, sticky='w')
            lbl_com_err_.grid(row=1, column=1, sticky='w')
            lbl_omi_err = Tk.Label(frm_left, text="Omission errors:", font=("Arial", 14))
            lbl_omi_err_ = Tk.Label(frm_left, text="{}".format(self._cs_data.omission_errors[WHOLE]), font=("Arial", 16), fg='coral')
            lbl_omi_err.grid(row=2, column=0, sticky='w')
            lbl_omi_err_.grid(row=2, column=1, sticky='w')
            lbl_oth_err = Tk.Label(frm_left, text="Other errors:", font=("Arial", 14))
            lbl_oth_err_ = Tk.Label(frm_left, text="{}".format(self._cs_data.other_errors[WHOLE]), font=("Arial", 16), fg='coral')
            lbl_oth_err.grid(row=3, column=0, sticky='w')
            lbl_oth_err_.grid(row=3, column=1, sticky='w')
            lbl_mean = Tk.Label(frm_left, text="Mean of RTs:", font=("Arial", 14))
            lbl_mean_ = Tk.Label(frm_left, text="{:.0f} ms".format(self._cs_data.mean[WHOLE]), font=("Arial", 16), fg='pale turquoise')
            lbl_mean.grid(row=4, column=0, sticky='w')
            lbl_mean_.grid(row=4, column=1, sticky='w')
            lbl_std_dev = Tk.Label(frm_left, text="Standard dev. of RTs:", font=("Arial", 14))
            lbl_std_dev_ = Tk.Label(frm_left, text="{:.0f} ms".format(self._cs_data.std_dev[WHOLE]), font=("Arial", 16), fg='light blue')
            lbl_std_dev.grid(row=5, column=0, sticky='w')
            lbl_std_dev_.grid(row=5, column=1, sticky='w')
            lbl_slope = Tk.Label(frm_left, text="Slope of reg. line:", font=("Arial", 14))
            lbl_slope_ = Tk.Label(frm_left, text="{:.2f}".format(self._cs_data.regression_line[1]), font=("Arial", 16), fg='lemon chiffon')
            lbl_slope.grid(row=6, column=0, sticky='w')
            lbl_slope_.grid(row=6, column=1, sticky='w')
            lbl_aus = Tk.Label(frm_left, text="Mean variance:", font=("Arial", 14))
            lbl_aus_ = Tk.Label(frm_left, text="{:.2f}".format(self._cs_data.aus[WHOLE]), font=("Arial", 16), fg='salmon')
            lbl_aus.grid(row=7, column=0, sticky='w')
            lbl_aus_.grid(row=7, column=1, sticky='w')

            #    RIGHT
            plt.style.use('dark_background')

            # response time graph
            fig_rt = plt.Figure(figsize=(7.52, 3), dpi=100, tight_layout=True)  # create a canvas to draw
            axes_rt = fig_rt.add_subplot(1, 1, 1)  # create an axes object add_subplot(nrows, ncols, index, **kwargs)
            axes_rt.set_title('Response times')
            axes_rt.set_ylim(RT_TIME_MIN, RT_TIME_MAX)
            axes_rt.set_xlim(0, self._cs_data.step_count[WHOLE])
            axes_rt.set_xlabel("Trial number")
            axes_rt.set_ylabel("RT (ms)")
            axes_rt.set_yticks(np.arange(RT_TIME_MIN, RT_TIME_MAX + 1, 100))
            # axes_rt.set_xticks(np.arange(0, self._cs_data.step_count[WHOLE] + 1, 9))
            axes_rt.xaxis.set_major_locator(MultipleLocator(18))
            axes_rt.xaxis.set_minor_locator(MultipleLocator(9))
            axes_rt.grid(which="minor", color='gray', linestyle='--', linewidth=0.5)
            axes_rt.grid(which="major", color='gray', linestyle='--', linewidth=0.5)
            axes_rt.axhspan(RESPONSE_CUE_START, RESPONSE_CUE_END, facecolor='white', alpha=0.4, label="response cue")
            x_rt = np.arange(0, self._cs_data.step_count[WHOLE])
            y_rt = self._cs_data.ms[WHOLE]
            axes_rt.bar(x_rt, y_rt, color='C0', label='user time', align='edge', width=1.0)
            x_rt_line = np.array([0, self._cs_data.step_count[WHOLE] - 1])
            y_rt_line = np.array(2 * [self._cs_data.regression_line[0]]) + x_rt_line * np.array(2 * [self._cs_data.regression_line[1]])  # once * for more elements, once * for vector multiplication ^^
            axes_rt.plot(x_rt_line, y_rt_line, color='C1', label="slope")
            axes_rt.legend()

            # means by digits graph
            fig_dig_means = plt.Figure(figsize=(3.5, 2.2), dpi=100, tight_layout=True)
            axes_dig_means = fig_dig_means.add_subplot(1, 1, 1)
            axes_dig_means.set_title('Means by digits')
            axes_dig_means.set_ylim(DGM_TIME_MIN, DGM_TIME_MAX)
            axes_dig_means.set_xlabel("Digits")
            axes_dig_means.set_ylabel("Mean RT (ms)")
            axes_dig_means.set_yticks(np.arange(DGM_TIME_MIN, DGM_TIME_MAX + 1, 100))
            axes_dig_means.set_xticks(DIGITS_EXCEPT_3)
            axes_dig_means.grid(color='gray', linestyle='--', linewidth=0.5)
            x_dig_means = DIGITS_EXCEPT_3
            y_dig_means = self._cs_data.mean_by_digit[WHOLE]
            axes_dig_means.bar(x_dig_means, y_dig_means, color="C2", label="mean RT", width=0.5)
            axes_dig_means.legend()
            # x_dig_means = range(len(DIGITS_EXCEPT_3))
            # axes_dig_means.set_xticks(x_dig_means)
            # axes_dig_means.set_xticklabels(DIGITS_EXCEPT_3)

            # fft graph
            fig_fft = plt.Figure(figsize=(4, 2.2), dpi=100, tight_layout=True)
            axes_fft = fig_fft.add_subplot(1, 1, 1)
            axes_fft.set_title('Variance spectrum')
            axes_fft.set_xlim(0, FREQ_MAX)
            axes_fft.set_ylim(0, FFT_TIME_MAX)
            axes_fft.set_xlabel("Frequency (Hz)")
            axes_fft.set_ylabel("Amplitude (ms)")
            axes_fft.set_xticks(np.arange(0, FREQ_MAX + 0.05, 0.05))
            axes_fft.minorticks_on()
            axes_fft.grid(color='gray', linestyle='--', linewidth=0.5)
            x_fft = self._cs_data.fft_freq[WHOLE]
            y_fft = self._cs_data.fft[WHOLE]
            axes_fft.plot(x_fft, y_fft, color="C3", label="amplitude")
            axes_fft.axvline(PSP_FREQ, color='rosybrown', linestyle='--', linewidth=0.5, label="sequence freq.")
            axes_fft.legend()
            # signal = self._cs_data.ms_interpolated[WHOLE]
            # axes_fft.psd(signal, Fs=1.0/1.439)

            # Prepare graphs for use with Tkinter
            cnvs_rt = FigureCanvasTkAgg(fig_rt, frm_right)
            cnvs_rt.draw()
            cnvs_dig_mean_1 = FigureCanvasTkAgg(fig_dig_means, frm_right)
            cnvs_dig_mean_1.draw()
            cnvs_fft_1 = FigureCanvasTkAgg(fig_fft, frm_right)
            cnvs_fft_1.draw()

            # tlbr_rt = NavigationToolbar2Tk(cnvs_rt, frm_results)
            # tlbr_rt.update()

            cnvs_rt.get_tk_widget().grid(row=0, columnspan=2)
            cnvs_dig_mean_1.get_tk_widget().grid(row=1, column=0, sticky='w')
            cnvs_fft_1.get_tk_widget().grid(row=1, column=1, sticky='w')
            # todo zvazit side, fill a expand, stejne i u toolbaru
            # cnvs_rt._tkcanvas.grid(row=5, column=1)

            # PLACE ALL THE STUFF AT ONCE FOR NICER APPEAR
            frm_left.grid(row=0, column=0, padx=(0, 30))
            frm_right.grid(row=0, column=1)
            lbl_header.grid(row=0)
            lbl_sub_header.grid(row=1, pady=(0, 10))
            frm_results.grid(row=2, pady=(0, 10))
            lbl_controls1.grid(row=3)
            lbl_controls2.grid(row=4)
            lbl_controls3.grid(row=5)

        else:
            # SHOWING RESULT OF THE CURRENT TEST
            if self._index is None or self._max_index is None:
                # TOP
                lbl_header = Tk.Label(parent, text="Half by half comparison", font=("Arial", 24))
                lbl_controls1 = Tk.Label(parent, text="Press Enter or space to switch to overall result",
                                         font=("Arial", 14))
                lbl_controls2 = Tk.Label(parent, text="Press R to go back to intro")
                lbl_controls3 = Tk.Label(parent, text="Press Esc to exit")
            # BROWSING PREVIOUSLY SAVED RESULTS
            else:
                lbl_header = Tk.Label(parent, text="Half by half comparison {} of {}".format(self._index, self._max_index),
                                      font=("Arial", 16))
                lbl_controls1 = Tk.Label(parent, text="Press Enter or space to switch to overall result")
                lbl_controls2 = Tk.Label(parent, text="Press Left / Right to browse results")
                lbl_controls3 = Tk.Label(parent, text="Press Esc to go back to intro")
            lbl_sub_header = Tk.Label(parent, text=(
                        self._cs_data.name + " " + str(self._cs_data.timestamp.strftime("%Y-%m-%d %H:%M:%S"))),
                                      font=("Arial", 14))

            frm_results = Tk.Frame(parent)

            frm_left = Tk.Frame(frm_results)
            frm_left.columnconfigure(0, weight=1, minsize=220)
            frm_left.columnconfigure(1, weight=1, minsize=70)
            frm_left.columnconfigure(2, weight=1, minsize=70)
            frm_left.columnconfigure(3, weight=1, minsize=70)

            frm_right = Tk.Frame(frm_results)

            #    LEFT
            lbl_first = Tk.Label(frm_left, text="First", font=("Arial", 12))
            lbl_first.grid(row=0, column=1)
            lbl_diff = Tk.Label(frm_left, text="Difference", font=("Arial", 12))
            lbl_diff.grid(row=0, column=2)
            lbl_second = Tk.Label(frm_left, text="Second", font=("Arial", 12))
            lbl_second.grid(row=0, column=3)

            lbl_com_err = Tk.Label(frm_left, text="Comission errors:", font=("Arial", 14))
            lbl_com_err.grid(row=1, column=0, sticky='w')
            lbl_com_err_1 = Tk.Label(frm_left, text="{}".format(self._cs_data.comission_errors[FIRST]), font=("Arial", 16), fg='coral')
            com_err_diff = self._cs_data.comission_errors[SECOND] - self._cs_data.comission_errors[FIRST]
            lbl_com_err_2 = Tk.Label(frm_left, text="{:+d}".format(com_err_diff), font=("Arial", 16), fg='brown1' if com_err_diff > 0 else 'medium sea green' if com_err_diff < 0 else 'white')
            lbl_com_err_3 = Tk.Label(frm_left, text="{}".format(self._cs_data.comission_errors[SECOND]), font=("Arial", 16), fg='coral')
            lbl_com_err_1.grid(row=1, column=1)
            lbl_com_err_2.grid(row=1, column=2)
            lbl_com_err_3.grid(row=1, column=3)

            lbl_omi_err = Tk.Label(frm_left, text="Omission errors:", font=("Arial", 14))
            lbl_omi_err.grid(row=2, column=0, sticky='w')
            lbl_omi_err_1 = Tk.Label(frm_left, text="{}".format(self._cs_data.omission_errors[FIRST]), font=("Arial", 16), fg='coral')
            omi_err_diff = self._cs_data.omission_errors[SECOND] - self._cs_data.omission_errors[FIRST]
            lbl_omi_err_2 = Tk.Label(frm_left, text="{:+d}".format(omi_err_diff), font=("Arial", 16), fg='brown1' if omi_err_diff > 0 else 'medium sea green' if omi_err_diff < 0 else 'white')
            lbl_omi_err_3 = Tk.Label(frm_left, text="{}".format(self._cs_data.omission_errors[SECOND]), font=("Arial", 16), fg='coral')
            lbl_omi_err_1.grid(row=2, column=1)
            lbl_omi_err_2.grid(row=2, column=2)
            lbl_omi_err_3.grid(row=2, column=3)

            lbl_oth_err = Tk.Label(frm_left, text="Other errors:", font=("Arial", 14))
            lbl_oth_err.grid(row=3, column=0, sticky='w')
            lbl_oth_err_1 = Tk.Label(frm_left, text="{}".format(self._cs_data.other_errors[FIRST]), font=("Arial", 16), fg='coral')
            oth_err_diff = self._cs_data.other_errors[SECOND] - self._cs_data.other_errors[FIRST]
            lbl_oth_err_2 = Tk.Label(frm_left, text="{:+d}".format(oth_err_diff), font=("Arial", 16), fg='brown1' if oth_err_diff > 0 else 'medium sea green' if oth_err_diff < 0 else 'white')
            lbl_oth_err_3 = Tk.Label(frm_left, text="{}".format(self._cs_data.other_errors[SECOND]), font=("Arial", 16), fg='coral')
            lbl_oth_err_1.grid(row=3, column=1)
            lbl_oth_err_2.grid(row=3, column=2)
            lbl_oth_err_3.grid(row=3, column=3)

            lbl_mean = Tk.Label(frm_left, text="Mean of RTs:", font=("Arial", 14))
            lbl_mean.grid(row=4, column=0, sticky='w')
            lbl_mean_1 = Tk.Label(frm_left, text="{:.0f} ms".format(self._cs_data.mean[FIRST]), font=("Arial", 16), fg='pale turquoise')
            mean_diff = self._cs_data.mean[SECOND] - self._cs_data.mean[FIRST]
            lbl_mean_2 = Tk.Label(frm_left, text="{:+.0f}".format(mean_diff), font=("Arial", 16), fg='brown1' if mean_diff > 0 else 'medium sea green' if mean_diff < 0 else 'white')
            lbl_mean_3 = Tk.Label(frm_left, text="{:.0f} ms".format(self._cs_data.mean[SECOND]), font=("Arial", 16), fg='pale turquoise')
            lbl_mean_1.grid(row=4, column=1)
            lbl_mean_2.grid(row=4, column=2)
            lbl_mean_3.grid(row=4, column=3)

            lbl_std_dev = Tk.Label(frm_left, text="Standard dev. of RTs:", font=("Arial", 14))
            lbl_std_dev.grid(row=5, column=0, sticky='w')
            lbl_std_dev_1 = Tk.Label(frm_left, text="{:.0f} ms".format(self._cs_data.std_dev[FIRST]), font=("Arial", 16), fg='light blue')
            std_dev_diff = self._cs_data.std_dev[SECOND] - self._cs_data.std_dev[FIRST]
            lbl_std_dev_2 = Tk.Label(frm_left, text="{:+.0f}".format(std_dev_diff), font=("Arial", 16), fg='brown1' if std_dev_diff > 0 else 'medium sea green' if std_dev_diff < 0 else 'white')
            lbl_std_dev_3 = Tk.Label(frm_left, text="{:.0f} ms".format(self._cs_data.std_dev[SECOND]), font=("Arial", 16), fg='light blue')
            lbl_std_dev_1.grid(row=5, column=1)
            lbl_std_dev_2.grid(row=5, column=2)
            lbl_std_dev_3.grid(row=5, column=3)

            lbl_aus = Tk.Label(frm_left, text="Mean variance:", font=("Arial", 14))
            lbl_aus.grid(row=6, column=0, sticky='w')
            lbl_aus_1 = Tk.Label(frm_left, text="{:.2f} ms".format(self._cs_data.aus[FIRST]), font=("Arial", 16), fg='salmon')
            aus_diff = self._cs_data.aus[SECOND] - self._cs_data.aus[FIRST]
            lbl_aus_2 = Tk.Label(frm_left, text="{:+.2f}".format(aus_diff), font=("Arial", 16), fg='brown1' if aus_diff > 0 else 'medium sea green' if aus_diff < 0 else 'white')
            lbl_aus_3 = Tk.Label(frm_left, text="{:.2f} ms".format(self._cs_data.aus[SECOND]), font=("Arial", 16), fg='salmon')
            lbl_aus_1.grid(row=6, column=1)
            lbl_aus_2.grid(row=6, column=2)
            lbl_aus_3.grid(row=6, column=3)

            #    RIGHT
            plt.style.use('dark_background')

            # 1st means by digits graph
            fig_dig_means_1 = plt.Figure(figsize=(3.5, 2.2), dpi=100, tight_layout=True)
            axes_dig_means_1 = fig_dig_means_1.add_subplot(1, 1, 1)
            axes_dig_means_1.set_title('Means by digits 1st')
            axes_dig_means_1.set_ylim(DGM_TIME_MIN, DGM_TIME_MAX)
            axes_dig_means_1.set_xlabel("Digits")
            axes_dig_means_1.set_ylabel("Mean RT (ms)")
            axes_dig_means_1.set_yticks(np.arange(DGM_TIME_MIN, DGM_TIME_MAX + 1, 100))
            axes_dig_means_1.set_xticks(DIGITS_EXCEPT_3)
            axes_dig_means_1.grid(color='gray', linestyle='--', linewidth=0.5)
            x_dig_means_1 = DIGITS_EXCEPT_3
            y_dig_means_1 = self._cs_data.mean_by_digit[FIRST]
            axes_dig_means_1.bar(x_dig_means_1, y_dig_means_1, color="C2", label="mean RT", width=0.5)
            axes_dig_means_1.legend()
            
            # 2nd means by digits graph
            fig_dig_means_2 = plt.Figure(figsize=(3.5, 2.2), dpi=100, tight_layout=True)
            axes_dig_means_2 = fig_dig_means_2.add_subplot(1, 1, 1)
            axes_dig_means_2.set_title('Means by digits 2nd')
            axes_dig_means_2.set_ylim(DGM_TIME_MIN, DGM_TIME_MAX)
            axes_dig_means_2.set_xlabel("Digits")
            axes_dig_means_2.set_ylabel("Mean RT (ms)")
            axes_dig_means_2.set_yticks(np.arange(DGM_TIME_MIN, DGM_TIME_MAX + 1, 100))
            axes_dig_means_2.set_xticks(DIGITS_EXCEPT_3)
            axes_dig_means_2.grid(color='gray', linestyle='--', linewidth=0.5)
            x_dig_means_2 = DIGITS_EXCEPT_3
            y_dig_means_2 = self._cs_data.mean_by_digit[SECOND]
            axes_dig_means_2.bar(x_dig_means_2, y_dig_means_2, color="C2", label="mean RT", width=0.5)
            axes_dig_means_2.legend()

            # 1st fft graph
            fig_fft_1 = plt.Figure(figsize=(3.5, 2.2), dpi=100, tight_layout=True)
            axes_fft_1 = fig_fft_1.add_subplot(1, 1, 1)
            axes_fft_1.set_title('Variance spectrum 1st')
            axes_fft_1.set_ylim(0, FFT_TIME_MAX)
            axes_fft_1.set_xlabel("Frequency (Hz)")
            axes_fft_1.set_ylabel("Amplitude (ms)")
            axes_fft_1.set_xticks(np.arange(0, FREQ_MAX + 0.05, 0.05))
            axes_fft_1.minorticks_on()
            axes_fft_1.grid(color='gray', linestyle='--', linewidth=0.5)
            x_fft_1 = self._cs_data.fft_freq[FIRST]
            y_fft_1 = self._cs_data.fft[FIRST]
            axes_fft_1.plot(x_fft_1, y_fft_1, color="C3", label="amplitude")
            axes_fft_1.axvline(PSP_FREQ, color='rosybrown', linestyle='--', linewidth=0.5, label="sequence freq.")
            axes_fft_1.legend()
            
            # 2nd fft graph
            fig_fft_2 = plt.Figure(figsize=(3.5, 2.2), dpi=100, tight_layout=True)
            axes_fft_2 = fig_fft_2.add_subplot(1, 1, 1)
            axes_fft_2.set_title('Variance spectrum 2nd')
            axes_fft_2.set_ylim(0, FFT_TIME_MAX)
            axes_fft_2.set_xlabel("Frequency (Hz)")
            axes_fft_2.set_ylabel("Amplitude (ms)")
            axes_fft_2.set_xticks(np.arange(0, FREQ_MAX + 0.05, 0.05))
            axes_fft_2.minorticks_on()
            axes_fft_2.grid(color='gray', linestyle='--', linewidth=0.5)
            x_fft_2 = self._cs_data.fft_freq[SECOND]
            y_fft_2 = self._cs_data.fft[SECOND]
            axes_fft_2.plot(x_fft_2, y_fft_2, color="C3", label="amplitude")
            axes_fft_2.axvline(PSP_FREQ, color='rosybrown', linestyle='--', linewidth=0.5, label="sequence freq.")
            axes_fft_2.legend()



            # Prepare graphs for use with Tkinter
            cnvs_dig_mean_1 = FigureCanvasTkAgg(fig_dig_means_1, frm_right)
            cnvs_dig_mean_1.draw()
            cnvs_dig_mean_2 = FigureCanvasTkAgg(fig_dig_means_2, frm_right)
            cnvs_dig_mean_2.draw()
            cnvs_fft_1 = FigureCanvasTkAgg(fig_fft_1, frm_right)
            cnvs_fft_1.draw()
            cnvs_fft_2 = FigureCanvasTkAgg(fig_fft_2, frm_right)
            cnvs_fft_2.draw()

            cnvs_dig_mean_1.get_tk_widget().grid(row=0, column=0, sticky='w')
            cnvs_dig_mean_2.get_tk_widget().grid(row=0, column=1, sticky='w')
            cnvs_fft_1.get_tk_widget().grid(row=1, column=0, sticky='w')
            cnvs_fft_2.get_tk_widget().grid(row=1, column=1, sticky='w')

            # PLACE ALL THE STUFF AT ONCE FOR NICER APPEAR
            frm_left.grid(row=0, column=0, padx=(0, 30))
            frm_right.grid(row=0, column=1)
            lbl_header.grid(row=0)
            lbl_sub_header.grid(row=1, pady=(0, 10))
            frm_results.grid(row=2, pady=(0, 10))
            lbl_controls1.grid(row=3)
            lbl_controls2.grid(row=4)
            lbl_controls3.grid(row=5)

    def set_data(self, data):
        # type: (Tuple[Optional[CSData], Optional[bool], Optional[int], Optional[int]]) -> None
        self._cs_data = data[0]
        self._halved = data[1]
        self._index = data[2]
        self._max_index = data[3]
