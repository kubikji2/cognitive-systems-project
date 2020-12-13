#!/usr/bin/python2

import Tkinter as Tk
from PIL import ImageTk, Image
from TkinterViewContent import TkinterViewContent

"""
An 50x50 image specified in image_path
"""
class TVCImage(TkinterViewContent):

    def __init__(self, cs_view, image_path):
        # base constructor call
        # it requires list of the keys to listen
        TkinterViewContent.__init__(self, cs_view)
        # load and save reference to image see http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        self.image_path = image_path
        img = Image.open(self.image_path)
        img = img.resize((50, 50), Image.LANCZOS)  # Image.NEAREST for fastest
        self.photo_img = ImageTk.PhotoImage(img)
        # todo consider image loading into some cache, to not load them again every time

    def show(self):
        # Create widgets
        my_label = Tk.Label(self.csv.frame, image=self.photo_img)
        # Show widgets
        my_label.pack()
