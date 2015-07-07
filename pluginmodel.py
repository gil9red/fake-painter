#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from PySide.QtCore import *


class PluginModel(QAbstractListModel):
    def __init__(self, data_singleton):
        super().__init__()

        self.data_singleton = data_singleton

        self.plugins = self.data_singleton.plugins
        self.disabled_plugins = self.data_singleton.disabled_plugins
        self.name_plugins = sorted(self.plugins.keys())

        self.checked_list = [None] * self.rowCount()

    def rowCount(self, parent=None):
        return len(self.name_plugins)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return

        i = index.row()
        name = self.name_plugins[i]

        if role == Qt.DisplayRole:
            return name

        elif role == Qt.CheckStateRole:
            if self.checked_list[i] is None:
                checked = Qt.Checked

                if name in self.disabled_plugins:
                    checked = Qt.Unchecked

                self.checked_list[i] = checked == Qt.Checked
                return checked
            else:
                return Qt.Checked if self.checked_list[i] else Qt.Unchecked

    def setData(self, index, value, role):
        if not index.isValid:
            return False

        if role == Qt.CheckStateRole:
            i = index.row()
            self.checked_list[i] = value == Qt.Checked

            self.dataChanged.emit(index, index)

            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable

    def get(self, index):
        return self.get_by_row(index.row())

    def get_by_row(self, row):
        name = self.name_plugins[row]
        return self.plugins[name]

    def is_checked(self, row):
        return self.checked_list[row]
