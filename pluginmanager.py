#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from pluginmanager_ui import Ui_PluginManager
from PySide.QtGui import *
from PySide.QtCore import *


class PluginManager(QDialog, QObject):
    def __init__(self, data_singleton, parent=None):
        super().__init__(parent)

        self.ui = Ui_PluginManager()
        self.ui.setupUi(self)

        self.data_singleton = data_singleton

    def accept(self, *args, **kwargs):
        # self.datasingleton.image.history_depth = self.ui.sbHistoryDepth.value()
        # self.datasingleton.image.base_width = self.ui.sbWidth.value()
        # self.datasingleton.image.base_height = self.ui.sbHeight.value()
        #
        # self.datasingleton.mainWindow.write_settings()

        super().accept()
