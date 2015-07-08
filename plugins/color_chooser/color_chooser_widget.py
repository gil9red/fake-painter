#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from PySide.QtGui import *
from PySide.QtCore import *


class ColorChooserWidget(QLabel):
    """Widget for selecting color."""

    def __init__(self, r, g, b):
        super().__init__()

        self.setFrameStyle(QFrame.Raised | QFrame.Box)
        self.setMargin(3)
        self.setAlignment(Qt.AlignHCenter)

        self._current_color = QColor(r, g, b)
        self._pixmap = QPixmap(20, 20)

        self.set_color(self._current_color)

    send_color = Signal(QColor)

    def set_color(self, color):
        self._current_color = color

        self._pixmap.fill(color)
        self.setPixmap(self._pixmap)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            color = QColorDialog.getColor(self._current_color, self)
            if color.isValid():
                self.set_color(color)
                self.send_color.emit(color)

        super().mousePressEvent(event)
