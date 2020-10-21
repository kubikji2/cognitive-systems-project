from Tkinter import *


class MainWindow:
    def __init__(self):
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

        # Create widgets
        middle_frame = Frame(self.window)
        my_label = Label(middle_frame, text="Hello world")

        # Show widgets
        middle_frame.place(relx=.5, rely=.5, anchor="center")
        my_label.pack()

    def run(self):
        self.window.mainloop()
        # alternative
        # while True:
        #     root.update_idletasks()
        #     root.update()


if __name__ == '__main__':
    app = MainWindow()
    app.run()

