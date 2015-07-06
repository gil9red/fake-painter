#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from iplugin import IPlugin
from PySide.QtGui import *


class PluginCursorPos(IPlugin):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton

        self.label = QLabel()

    def name(self):
        return 'Cursor Pos'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Cursor Pos'

    def initialize(self):
        mw = self.data_singleton.mainWindow
        mw.ui.statusbar.addWidget(self.label)
        # mw.ui.statusbar.addPermanentWidget(self.label, 1)

        mw.send_cursor_pos.connect(lambda x, y: self.label.setText('{}, {}'.format(x, y)))

    def destroy(self):
        # TODO: поддержать
        pass
