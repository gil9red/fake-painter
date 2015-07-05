#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from mainwindow import MainWindow
# import json


class DataSingleton:
    """
    Singleton for variables needed for the program.
    """

    def __init__(self):
        self.current_instrument = None
        self.action_inst_dict = {}
        # self.instActionDict = {}
        self.action_filter_dict = {}

        self.disabled_plugins = []

        # TODO: пусть синглетон будет хранить словари с плагинами -- проще
        # будет получать информацию из плагинов, да и идентичность объектов
        # в словарях pluginsloader и синглетона будет плюсом
        # # Словарь с загруженными плагинами: ключ - имя плагина,
        # # значение - экземпляр плагина
        # self.plugins = {}
        #
        # # Словарь с плагинами, которые были отключены пользователем: ключ - имя плагина,
        # # значение - экземпляр плагина
        # self.disabled_plugins = {}

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

    # TODO: rem
    # def to_json(self):
    #     return json.dumps(self.to_serialize(), indent=4)
    #
    # def from_json(self, json_str):
    #     data = json.loads(json_str)
    #     self.from_serialize(data)

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


instance = DataSingleton()
