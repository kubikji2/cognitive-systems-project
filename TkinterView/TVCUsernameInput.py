#!/usr/bin/python2

import Tkinter as Tk
from TkinterViewContent import TkinterViewContent

"""
Intruductory View content
"""
class TVCUsernameInput(TkinterViewContent):

    def __init__(self):
        self._ent_username = None

    def show(self, parent):
        # Create widgets
        lbl_header = Tk.Label(parent, text="Please type your name or nickname", font=("Arial", 24))
        self._ent_username = Tk.Entry(parent, width=30, justify='center', font=("Arial", 16, 'bold'), relief=Tk.FLAT)
        self._ent_username.focus()
        lbl_controls = Tk.Label(parent, text="Press Enter to confirm", font=("Arial", 16))
        lbl_controls2 = Tk.Label(parent, text="Press Esc to go back")

        # Place widgets
        lbl_header.grid(row=0, column=0, pady=(0, 30))
        self._ent_username.grid(row=1, column=0, pady=(0, 30))
        lbl_controls.grid(row=2, column=0)
        lbl_controls2.grid(row=3, column=0)

    def read_input(self):
        return self._ent_username.get()
