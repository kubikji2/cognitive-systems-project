#!/usr/bin/env python 

from TkinterView.TkinterView import TkinterView
from CSEventSystem import CSEventSystem
from CSData import CSData
from CSPresenter import CSPresenter

if __name__ == '__main__':

    # This app works in a MVP-like pattern.
    # Presenter is the main boss here. It tells view what to view. It creates and owns instances of the data model.
    # It also tells when to process the data, and passes various data to view through itself.

    event_system = CSEventSystem()  # a way for VIEW to communicate back to PRESENTER
    view = TkinterView(event_system)  # VIEW  (ES - triggering events)
    presenter = CSPresenter(view, event_system)  # PRESENTER  (VIEW - direct control of it, ES - registering for events)

    presenter.start()  # start presenting the test
