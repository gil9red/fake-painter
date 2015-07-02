#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from settings_ui import Ui_Settings
from PySide.QtGui import *
from PySide.QtCore import *

# import datasingleton
# print(dir(datasingleton))
# from datasingleton import data_singleton as data_singleton


class Settings(QDialog, QObject):
    def __init__(self, datasingleton, parent=None):
        super().__init__(parent)

        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        self.datasingleton = datasingleton

        # self.ui.sbWidth.setValue(int(self.datasingleton.Image.base_width))
        # self.ui.sbHeight.setValue(int(self.datasingleton.Image.base_height))
        #
        # self.ui.sbHistoryDepth.setValue(int(self.datasingleton.Image.history_depth))

        self.ui.sbWidth.setValue(int(self.datasingleton.image.base_width))
        self.ui.sbHeight.setValue(int(self.datasingleton.image.base_height))

        self.ui.sbHistoryDepth.setValue(int(self.datasingleton.image.history_depth))

        # TODO: шаблоны как в гимпе

    def accept(self, *args, **kwargs):
        self.datasingleton.image.history_depth = self.ui.sbHistoryDepth.value()
        self.datasingleton.image.base_width = self.ui.sbWidth.value()
        self.datasingleton.image.base_height = self.ui.sbHeight.value()

        self.datasingleton.mainWindow.write_settings()
        # # # TODO: путь к файлу настроек брать из синглетона
        # ini = QSettings('settings.ini', QSettings.IniFormat)
        # self.datasingleton.write(ini)

        super().accept()