#!/usr/bin/python2

from TkinterView.TkinterView import TkinterView
from CSEventSystem import CSEventSystem
from CSData import CSData
from CSPresenter import CSPresenter

if __name__ == '__main__':

    event_system = CSEventSystem()  # a way for view to communicate back to presenter
    view = TkinterView(event_system)  # VIEW
    data = CSData()  # MODEL
    presenter = CSPresenter(view, event_system, data)  # PRESENTER

    presenter.start()  # start presenting the test
