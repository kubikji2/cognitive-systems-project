import Tkinter as Tk
from PIL import ImageTk, Image
from TkinterViewContent import TkinterViewContent

"""
An 50x50 image specified in image_path
"""
class TVCImage(TkinterViewContent):

    def __init__(self, image_path):
        # load and save reference to image see http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        self.image_path = image_path
        img = Image.open(self.image_path)
        img = img.resize((50, 50), Image.LANCZOS)  # Image.NEAREST for fastest
        self.photo_img = ImageTk.PhotoImage(img)  # IMPORTANT - need to keep theis references not only because speed, but also so that Python doesnt garbage collect the picture

    def show(self, parent):
        # Create widgets
        my_label = Tk.Label(parent, image=self.photo_img)
        # Show widgets
        my_label.pack()
