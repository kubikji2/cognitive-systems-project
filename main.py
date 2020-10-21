from Tkinter import *


class MainWindow:
    def __init__(self):
        # init root window
        self.window = Tk()
        self.window.attributes('-fullscreen', True)
        self.window.title("SART test")
        self.window.tk_setPalette(background="black", foreground="white")

        # Bind keypresses
        self.window.bind("<F11>",
                         lambda event: self.window.attributes("-fullscreen", not self.window.attributes("-fullscreen")))
        self.window.bind("<Escape>",
                         lambda event: self.window.attributes("-fullscreen", False))

        # Create widgets
        myLabel = Label(self.window, text="Hello world")
        # Add widgets
        myLabel.pack()

    def run(self):
        self.window.mainloop()
        # alternative
        # while True:
        #     root.update_idletasks()
        #     root.update()


if __name__ == '__main__':
    app = MainWindow()
    app.run()

