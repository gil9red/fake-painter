#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from iplugin import IPlugin
from PySide.QtGui import QLabel


class PluginSizeCanvasIndicator(IPlugin):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton
        self.label = QLabel()
        self.mw = self.data_singleton.mainWindow

    def name(self):
        return 'Size Canvas Indicator'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Size Canvas Indicator'

    def initialize(self):
        self.label.setVisible(True)
        self.mw.ui.statusbar.addWidget(self.label)
        # self.mw.ui.statusbar.addPermanentWidget(self.label, 1)

        self.mw.send_new_image_size.connect(self.update_label)

        canvas = self.mw.get_current_canvas()
        if canvas is not None:
            self.update_label(canvas.width(), canvas.height())

    def destroy(self):
        self.mw.ui.statusbar.removeWidget(self.label)
        self.mw.send_new_image_size.disconnect(self.update_label)

    def update_label(self, w, h):
        self.label.setText('{} x {}'.format(w, h))
