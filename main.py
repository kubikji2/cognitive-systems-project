#!/usr/bin/python2

from Tkinter import *

MOUSE_LABEL = "<Button-1>"

"""
CSWindow (Cognitive Systems Windows) creates Tkinter window.
Inside CSWindow the current CSWindowContent is drawn (see CSWindowContent class for futher details)
CSWindow take care of propagating user inputs (events) to the CSWindowContent via binding and unbinding
"""
class CSWindow:
   
    def __init__(self):
        # manage keyboard and mouse input
        self._set_window()
        self._set_frame()

        self.content = FALSE

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
    
    def _set_frame(self):
        self.frame = Frame(self.window)

    def run(self):
        self.window.mainloop()
        # alternative
        # while True:
        #     root.update_idletasks()
        #     root.update()

    
    def set_content(self,content):
        if(self.content):
            self.content.unbind()
        
        self.content = content
        
        self._clear_frame()
        self.content.bind()
        self.content.draw()

    # clear frame
    # based on:
    # https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
    def _clear_frame(self):
        # destroy all widgets from frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        self.frame.pack_forget()

"""
This abstract class take care of content shown in the CSWindow.
Each inherited class should be named in format CSWC+Name
Content requires window to draw into.
If there are any keyboard keys used as input, pass them in the constructor.
"""
class CSWindowContent:

    def __init__(self, cs_window, keys = []):
        # window I am drawing into
        self.cs_window = cs_window
        self.window = cs_window.window
        
        # keys I will be listening
        self.keys = keys

        # handler function ids, based on:
        # https://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding
        self.key_fids = []
        self.mouse_fid = -1
    
    def bind(self):
        # binding mouse
        self.mouse_fid = self.window.bind(MOUSE_LABEL, self.mouse_callback)

        # binding keys
        for i in range(len(self.keys)):
            key = self.keys[i]
            print(">>>",self, " binding key ", key)
            #callback = self.key_callbacks[i]
            fid = self.window.bind(key, lambda event : self.key_callback(event))
            self.key_fids.append(fid)

    def unbind(self):
        # unbind mouse
        self.window.unbind(MOUSE_LABEL, self.mouse_fid)

        # unbind keys
        for i in range(len(self.keys)):
            key = self.keys[i]
            fid = self.key_fids[i]
            self.window.unbind(key,fid)

    def key_callback(self, event):
        print("TBD")

    def mouse_callback(self,event):
        print("TBD")

    def touch_screen_callback(self,event):
        print("TBD")

    def handle_xy(self,x,y):
        print("TBD")

class CSWCTest(CSWindowContent):
    def __init__(self, window):
        # base constructor call
        # it requires list of the keys to listen
        CSWindowContent.__init__(self, window, ["a","s","d","w","<Return>"])

        print(self.window)
        
    def draw(self):
        # Create widgets
        # frame je vlastne jen seskupovac vicero widgetu ktere tvori nejaky celek, abych s nimi mohl napr hybat najednou
        my_label = Label(self.cs_window.frame, text="Hello world")

        # Show widgets
        self.cs_window.frame.place(relx=.5, rely=.5, anchor="center")
        my_label.pack()
        

    def key_callback(self, event):
        print("key: " + event.char)

    def mouse_callback(self,event):
        print("mouse clicked at ["+str(event.x)+","+str(event.y)+"]")

    

class CSWCIntro(CSWindowContent):

    def __init__(self, cs_window):
        # base constructor call
        # it requires list of the keys to listen
        CSWindowContent.__init__(self, cs_window, ["t"])

        print("window", self.window, cs_window)
        
    def draw(self):
        # Create widgets
        # frame je vlastne jen seskupovac vicero widgetu ktere tvori nejaky celek, abych s nimi mohl napr hybat najednou
        my_label = Label(self.cs_window.frame, text="Welcome. Press Enter (TBD) to continue, Esc to exit, T for testing context")

        # Show widgets
        self.cs_window.frame.place(relx=.5, rely=.5, anchor="center")
        my_label.pack()

    def key_callback(self, event):
        print("key: " + event.char)
        if(event.char == "t"):
            self.cs_window.set_content(CSWCTest(self.cs_window))

    def mouse_callback(self,event):
        print("mouse clicked at ["+str(event.x)+","+str(event.y)+"]")

if __name__ == '__main__':
    app = CSWindow()
    app.set_content(CSWCIntro(app))
    app.run()

