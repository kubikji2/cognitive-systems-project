#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent
from CSData import *
from typing import Optional, Union

import matplotlib
matplotlib.use("TkAgg")  # setting matplotlib to use the 'Tkinter Anti-grain renderer' backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.figure as plot  # diference of pyplot and figure here: https://stackoverflow.com/questions/5450207/whats-the-difference-between-matplotlib-pyplot-and-matplotlib-figure

"""
Screen showing the results to the user
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
            err1 = Tk.Label(parent, text="Press R to try again")
            err2 = Tk.Label(parent, text="Press Esc to go back")
            err.pack()
            err1.pack()
            err2.pack()
            return

        # todo implement screen with halves
        if self._halved:
            lbl_debug = Tk.Label(parent, text="Halved")
            lbl_debug.pack()

        # SHOWING RESULT OF THE CURRENT TEST
        if self._index is None or self._max_index is None:
            # TOP
            lbl_header = Tk.Label(parent, text="Overall result", font=("Arial", 24))
            lbl_controls2 = Tk.Label(parent, text="Press R to go back to intro")
            lbl_controls3 = Tk.Label(parent, text="Press Esc to exit")
        # BROWSING PREVIOUSLY SAVED RESULTS
        else:
            lbl_header = Tk.Label(parent, text="Result {} of {}".format(self._index, self._max_index), font=("Arial", 16))
            lbl_controls2 = Tk.Label(parent, text="Press Esc to go back to intro")
            lbl_controls3 = Tk.Label(parent, text="")
        lbl_sub_header = Tk.Label(parent, text=(self._cs_data.get_name() + " " + str(self._cs_data.get_timestamp().strftime("%Y-%m-%d %H:%M:%S"))), font=("Arial", 14))


        # middle
        frm_results = Tk.Frame(parent)
        frm_left = Tk.Frame(frm_results)
        frm_right = Tk.Frame(frm_results)

        #    left
        lbl_count = Tk.Label(frm_left, text="Total trials: {}".format(self._cs_data.get_step_count()[WHOLE]), font=("Arial", 16))
        lbl_mean = Tk.Label(frm_left, text="Mean RT (respnonse time): {:.0f} ms".format(self._cs_data.get_mean()[WHOLE]), font=("Arial", 16))
        lbl_std_dev = Tk.Label(frm_left, text="Standart deviation of RT: {:.0f} ms".format(self._cs_data.get_std_dev()[WHOLE]), font=("Arial", 16))
        lbl_com_err = Tk.Label(frm_left, text="Comission errors (presses on '3'): {}".format(self._cs_data.get_comission_errors()[WHOLE]), font=("Arial", 16))
        lbl_omi_err = Tk.Label(frm_left, text="Omission errors (missed presses): {}".format(self._cs_data.get_omission_errors()[WHOLE]), font=("Arial", 16))
        lbl_rnd_err = Tk.Label(frm_left, text="Other errors (multiple/early/late presses): {}".format(self._cs_data.get_comission_errors()[WHOLE]), font=("Arial", 16))

        #    right
        fig_rt = plot.Figure(figsize=(4, 3), dpi=100)  # create a canvas to draw
        axes_rt = fig_rt.add_subplot(111)  # create an axes object
        axes_rt.set_title('Response times')
        x_rt = self._cs_data.get_step_nums_stripped()[WHOLE]
        y_rt = self._cs_data.get_ms_stripped()[WHOLE]
        axes_rt.bar(x_rt, y_rt)
        # axes_rt.plot(x_rt, y_rt)  # , kind='bar', legend=True from pyplot

        cnvs_rt = FigureCanvasTkAgg(fig_rt, frm_right)
        cnvs_rt.draw()

        tlbr_rt = NavigationToolbar2Tk(cnvs_rt, frm_right)
        tlbr_rt.update()


        # bottom
        lbl_controls = Tk.Label(parent, text="Press Enter or space to switch to half-by-half comparison", font=("Arial", 16))


        # Show widgets
        lbl_header.pack()
        lbl_sub_header.pack(pady=(0, 5))

        frm_results.pack()
        frm_left.pack(side=Tk.LEFT)
        frm_right.pack(side=Tk.LEFT)

        lbl_count.pack()
        lbl_mean.pack()
        lbl_std_dev.pack()
        lbl_com_err.pack()
        lbl_omi_err.pack()
        lbl_rnd_err.pack()

        cnvs_rt._tkcanvas.pack()
        cnvs_rt.get_tk_widget().pack()  # todo zvazit side, fill a expand, stejne i u toolbaru

        lbl_controls.pack()
        lbl_controls2.pack()
        lbl_controls3.pack()

    def set_data(self, data):
        # type: (Tuple[Optional[CSData], Optional[bool], Optional[int], Optional[int]]) -> None
        self._cs_data = data[0]
        self._halved = data[1]
        self._index = data[2]
        self._max_index = data[3]



# # todo debug temporary
# def plot_regression_line(x, y, b):
#     # plotting the actual points as scatter plot
#     plt.scatter(x, y, color="m",
#                 marker="o", s=30)
#
#     # predicted response vector
#     y_pred = b[0] + b[1] * x
#
#     # plotting the regression line
#     plt.plot(x, y_pred, color="g")
#
#     # putting labels
#     plt.xlabel('x')
#     plt.ylabel('y')
#
#     # function to show plot
#     plt.show()
