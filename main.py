#!/usr/bin/python2

from Tkinter import *

from CSWindow import CSWindow
from CSWindowContent import CSWindowContent
from CSWCTest import *
from CSWCIntro import *

if __name__ == '__main__':
    app = CSWindow()
    app.set_content(CSWCIntro(app))
    app.run()

