#!/usr/bin/python2

import Tkinter as Tk
from PIL import ImageTk, Image
from TkinterViewContent import TkinterViewContent

"""

"""
class TVCInstructions(TkinterViewContent):

    def __init__(self):
        img_mask = Image.open("Images/mask.png")
        img_response = Image.open("Images/response.png")
        img_fixation = Image.open("Images/fixation.png")
        img_mask = img_mask.resize((50, 50), Image.LANCZOS)  # Image.NEAREST for fastest
        img_response = img_response.resize((50, 50), Image.LANCZOS)  # Image.NEAREST for fastest
        img_fixation = img_fixation.resize((50, 50), Image.LANCZOS)  # Image.NEAREST for fastest
        # IMPORTANT - need to keep these references not only because speed, but also so that Python doesnt garbage collect them
        self._pim_mask = ImageTk.PhotoImage(img_mask)
        self._pim_response = ImageTk.PhotoImage(img_response)
        self._pim_fixation = ImageTk.PhotoImage(img_fixation)

    def show(self, parent):
        # Create widgets
        lbl_header = Tk.Label(parent, text="Instructions", font=("Arial", 30))
        lbl_instructions = Tk.Message(parent, width=600, font=("Arial", 14), justify=Tk.CENTER, text="""
You will be presented with digits 1 to 9. The digits will appear in sequential order and repeat many times. Choose any key on your keyboard which is easy for you to press. Your task is to press your chosen key in response to each digit, except for when the digit is a '3'. 

For example, if you have chosen Enter and see the digit '1', press Enter. If you see the digit '3', DO NOT press anything.

To be more specific, each digit will be followed by a circle with a cross. The cross will then blink bold, which indicates when you should respond to the digit you just saw. You should not respond before the cricle appears - try to respond exactly on the indication, not sooner, nor later. Lastly, there will be a simple cross without circle marking preparation time for next digit.
        """)
        lbl_controls1 = Tk.Label(parent, font=("Arial", 16), text="Press Enter or Space to start a training block")
        lbl_controls2 = Tk.Label(parent, text="Press R to skip training")
        lbl_controls3 = Tk.Label(parent, text="Press Esc to go back to intro")

        frm_images = Tk.Frame(parent)
        lbl_digit = Tk.Label(frm_images, text="1", font=("Arial",  48))
        lbl_mask = Tk.Label(frm_images, image=self._pim_mask)
        lbl_response = Tk.Label(frm_images, image=self._pim_response)
        lbl_mask_after = Tk.Label(frm_images, image=self._pim_mask)
        lbl_fixation = Tk.Label(frm_images, image=self._pim_fixation)

        # Place widgets
        lbl_digit.pack(side='left')
        lbl_mask.pack(side='left')
        lbl_response.pack(side='left')
        lbl_mask_after.pack(side='left')
        lbl_fixation.pack(side='left')

        lbl_header.grid(row=0, pady=(0, 10))
        lbl_instructions.grid(row=1)
        frm_images.grid(row=2, pady=(0, 30))
        lbl_controls1.grid(row=3)
        lbl_controls2.grid(row=4)
        lbl_controls3.grid(row=5)
