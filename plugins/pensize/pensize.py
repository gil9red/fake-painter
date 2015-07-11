#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from iplugin import IPlugin
from PySide.QtGui import *


class PluginPenSize(IPlugin):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton

        self.mw = self.data_singleton.mainWindow
        self.size = None

    def name(self):
        return 'Pen Size'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Pen Size'

    def initialize(self):
        self.size = QSpinBox()
        self.size.setRange(1, 999)
        self.size.setValue(self.data_singleton.pen_size)

        self.size.valueChanged.connect(self.change_size)

        self.mw.ui.generalToolBar.addWidget(self.size)

    def destroy(self):
        self.size.deleteLater()
        self.size = None

    def change_size(self, value):
        self.data_singleton.pen_size = value
