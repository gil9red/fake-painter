#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from PySide.QtCore import QAbstractListModel

# TODO: закончить модель плагинов
class PluginModel(QAbstractListModel):
    def __init__(self, data_singleton):
        super().__init__()

        self.data_singleton = data_singleton

    def rowCount(self, *args, **kwargs):
        pass

    def data(self, *args, **kwargs):
        pass
