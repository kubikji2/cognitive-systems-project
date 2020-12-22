import Tkinter as Tk
from CSViewContent import CSViewContent

"""
CSVC For Testing Purposes - you can do anything you want with this
"""
class CSVCForTestingPurposes(CSViewContent):

    def __init__(self, cs_view):
        # base constructor call
        # it requires list of the keys to listen
        CSViewContent.__init__(self, cs_view, ['<Return>', '<space>', '<Button-1>'])

    def show(self):
        # Create widgets
        my_label = Tk.Label(self.csv.frame, text="Welcome. Press Enter or Space to start the test, Esc to exit")

        # Show widgets
        my_label.pack()

    def key_callback(self, event):
        print("key: " + repr(event.char))
        if event.char == '\r' or event.char == ' ':
            self.csv.cs_event_system.trigger("action")

    def mouse_callback(self, event):
        print("mouse clicked at [" + str(event.x) + "," + str(event.y) + "]")
