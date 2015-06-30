#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from mainwindow import MainWindow


class DataSingleton:
    """
    Singleton for variables needed for the program.
    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataSingleton, cls).__new__(cls)
        return cls.instance

    # def triggered_action_instrument(action):
    #     instrument = DataSingleton.actionInstDict[action]
    #     DataSingleton.currentInstrument = instrument

    currentInstrument = None
    actionInstDict = {}
    # instActionDict = {}

DataSingleton.mainWindow = MainWindow(DataSingleton)
DataSingleton.mainWindow.load_plugins()
