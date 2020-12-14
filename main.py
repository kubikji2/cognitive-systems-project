#!/usr/bin/python2

from TkinterView.TkinterView import TkinterView
from CSEventSystem import CSEventSystem
from CSData import CSData
from CSPresenter import CSPresenter

if __name__ == '__main__':

    event_system = CSEventSystem()  # a way for VIEW to communicate back to PRESENTER
    model = CSData()  # MODEL
    view = TkinterView(event_system, model)  # VIEW  (ES - triggering events, MODEL - getting collected data to view them)
    presenter = CSPresenter(view, event_system, model)  # PRESENTER  (VIEW - direct control of it, ES - registering for events, MODEL - writing data to it and controlling when to compute)

    presenter.start()  # start presenting the test
