import Tkinter as Tk
from CSViewContent import CSViewContent


"""
Intruductory Windows content
"""
class CSVCResults(CSViewContent):

    def __init__(self, cs_view):
        # base constructor call
        # it requires list of the keys to listen
        CSViewContent.__init__(self, cs_view, ['r'])

    def show(self):
        # Create widgets
        my_label = Tk.Label(self.csv.frame, text="Congratulations on finishing the test! Press R to restart or Esc to save results and quit")

        # Show widgets
        my_label.pack()

    def key_callback(self, event):
        if event.char == 'r':
            self.csv.cs_event_system.trigger("action_alt")

    def mouse_callback(self, event):
        pass
