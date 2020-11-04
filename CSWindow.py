#!/usr/bin/python2

from Tkinter import *

MOUSE_LABEL = "<Button-1>"

"""
CSWindow (Cognitive Systems Windows) creates Tkinter window.
Inside CSWindow the current CSWindowContent is drawn (see CSWindowContent class for futher details).
CSWindow take care of propagating user inputs (events) to the CSWindowContent via binding and unbinding them and also redrawing whether new content is set via set_content method.
"""
class CSWindow:
   
    def __init__(self):
        # manage keyboard and mouse input
        self._set_window()
        self._set_frame()

        self.content = FALSE

    # private-like (do not use outside of this class)
    # set up window
    def _set_window(self):
        # init root window
        self.window = Tk()
        self.window.geometry("800x600")
        # self.window.eval('tk::PlaceWindow . center')  # place the windowed version to center of screen
        self.window.attributes('-fullscreen', True)
        self.window.title("SART test")
        self.window.tk_setPalette(background="black", foreground="white")

        # Bind keypresses
        self.window.bind("<F11>",
                         lambda event: self.window.attributes("-fullscreen", not self.window.attributes("-fullscreen")))
        self.window.bind("<Escape>",
                         lambda event: self.window.destroy())
    
    # private-like (do not use outside of this class)
    # prepare frame 
    def _set_frame(self):
        self.frame = Frame(self.window)

    # run the app
    def run(self):
        self.window.mainloop()
        # alternative
        # while True:
        #     root.update_idletasks()
        #     root.update()

    
    # public-like
    # set new CSWindow Content
    # '-> unbind previous input control
    # '-> set new content
    # '-> clear frame
    # '-> bind new input control
    def set_content(self,content):
        if(self.content):
            self.content.unbind()
        
        self.content = content
        
        self.clear_frame()
        self.content.bind()
        self.content.draw()

    # public-like
    # clears frame
    # '-> destroy all widgets
    # '-> TODO: clear all drawn elements too maybe?
    # based on:
    # https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
    def clear_frame(self):
        # destroy all widgets from frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        self.frame.pack_forget()