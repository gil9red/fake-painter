#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtGui import *
from PySide.QtCore import *

class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.pressed = False
        self.image = QImage()
        self.x = None
        self.y = None

    def mouseMoveEvent(self, event):
        if self.pressed:
            self.x = event.pos().x()
            self.y = event.pos().y()

            self.update()

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        print('press')
        self.pressed = True

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressed = False

        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        if self.pressed:
            p = QPainter(self)
            p.setRenderHint(QPainter.Antialiasing)
            p.setPen(QPen(Qt.black, 5.0))

            p.drawPoint(self.x, self.y)

        super().paintEvent(event)