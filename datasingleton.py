#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from mainwindow import MainWindow
# from PySide.QtCore import *

print('datasingleton module')

# class Singleton(type):
#     _instances = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


import json


class DataSingleton:
    """
    Singleton for variables needed for the program.
    """

    def __init__(self):
        self.currentInstrument = None
        self.actionInstDict = {}
        # self.instActionDict = {}

        self.settings_path = 'settings.cfg'

        self.image = DataSingleton.Image()

        self.mainWindow = MainWindow(self)
        self.mainWindow.load_plugins()
        self.mainWindow.read_settings()
        # TODO: удалить, пусть по умолчанию редактор пустой
        self.mainWindow.new_tab()

    def to_serialize(self):
        return {
            'settings_path': self.settings_path,
            'image': self.image.to_serialize()
        }

    def from_serialize(self, data):
        self.settings_path = data['settings_path']
        self.image.from_serialize(data['image'])

    def to_json(self):
        return json.dumps(self.to_serialize(), indent=4)

    def from_json(self, json_str):
        data = json.loads(json_str)
        self.from_serialize(data)

    class Image:
        def __init__(self):
            self.history_depth = 40
            self.base_width = 640
            self.base_height = 480

        def to_serialize(self):
            return {
                'history_depth': self.history_depth,
                'base_width': self.base_width,
                'base_height': self.base_height
            }

        def from_serialize(self, data):
            self.history_depth = data['history_depth']
            self.base_width = data['base_width']
            self.base_height = data['base_height']


    # def to_JSON(self):
    #     import json
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    # class Image:
    #     def __init__(self):
    #         self.history_depth = 40
    #         self.base_width = 640
    #         self.base_height = 480


instance = DataSingleton()

# import jsonpickle
# frozen = jsonpickle.encode(data_singleton)
# print(frozen)

# import json
# # write the serialized data in the file
# with open('dataSingleton.pkl', 'wb') as f:
#     json.dump(dataSingleton.__dict__, f)

# print(pickle.dumps(dataSingleton))
# import json
# print(json.dumps(dataSingleton, cls=DataSingleton, skipkeys=True))

# dataSingleton.mainWindow = MainWindow(DataSingleton)
# dataSingleton.mainWindow.load_plugins()
# dataSingleton.mainWindow.read_settings()

# class DataSingleton:
#     """
#     Singleton for variables needed for the program.
#     """
#
#     def __new__(cls):
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(DataSingleton, cls).__new__(cls)
#         return cls.instance
#
#     # def triggered_action_instrument(action):
#     #     instrument = DataSingleton.actionInstDict[action]
#     #     DataSingleton.currentInstrument = instrument
#
#     currentInstrument = None
#     actionInstDict = {}
#     # instActionDict = {}
#
#     class Image:
#         history_depth = 40
#         base_width = 640
#         base_height = 480
#
#     @classmethod
#     def read(cls, ini):
#         ini.beginGroup('Image')
#         ini.setValue('history_depth', cls.Image.history_depth)
#         ini.setValue('base_width', cls.Image.base_width)
#         ini.setValue('base_height', cls.Image.base_height)
#         ini.endGroup()
#
#     @classmethod
#     def write(cls, ini):
#         ini.beginGroup('Image')
#         cls.Image.history_depth = ini.value('history_depth', 40)
#         cls.Image.base_width = ini.value('base_width', 640)
#         cls.Image.base_height = ini.value('base_height', 480)
#         ini.endGroup()
#
# DataSingleton.mainWindow = MainWindow(DataSingleton)
# DataSingleton.mainWindow.load_plugins()
# DataSingleton.mainWindow.read_settings()
