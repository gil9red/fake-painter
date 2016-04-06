#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from PySide.QtGui import QWidget, QHBoxLayout
from iplugin import IPlugin
from .color_chooser_widget import ColorChooserWidget

# TODO: tool tip: color1 -- карандаш, линии, линии фигур
# TODO: tool tip: color2 -- ластик, brush фигур


class PluginColorChooser(IPlugin):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton

        self.mw = self.data_singleton.mainWindow

        self._widget = None
        self._primary_color_chooser = None
        self._secondary_color_chooser = None

    def name(self):
        return 'Color Chooser'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Color Chooser'

    def initialize(self):
        color1 = self.data_singleton.primary_color
        color2 = self.data_singleton.secondary_color

        self._primary_color_chooser = ColorChooserWidget(color1)
        self._secondary_color_chooser = ColorChooserWidget(color2)

        self._primary_color_chooser.send_color.connect(self.set_primary_color)
        self._secondary_color_chooser.send_color.connect(self.set_secondary_color)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._primary_color_chooser)
        layout.addWidget(self._secondary_color_chooser)
        layout.addStretch()

        self._widget = QWidget()
        self._widget.setLayout(layout)

        self.mw.ui.generalToolBar.addWidget(self._widget)

    def destroy(self):
        self._widget.deleteLater()
        self._widget = None

        self._primary_color_chooser = None
        self._secondary_color_chooser = None

    def set_primary_color(self, color):
        self.data_singleton.primary_color = color

    def set_secondary_color(self, color):
        self.data_singleton.secondary_color = color
