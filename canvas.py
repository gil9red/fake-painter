#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtGui import *
from PySide.QtCore import *

class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.pressed = False
        # self.image = None
        self.image = QImage(400, 400, QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)

    # def resizeEvent(self, event):
    #     if self.image:
    #         self.image = self.image.copy(0, 0, event.size().width(), event.size().height())
    #     else:
    #         self.image = QImage(event.size(), QImage.Format_ARGB32)
    #         self.image.fill(Qt.transparent)
    #
    #     super().resizeEvent(event)

    def mouseMoveEvent(self, event):
        if self.pressed:
            x = event.pos().x()
            y = event.pos().y()

            p = QPainter(self.image)
            p.setRenderHint(QPainter.Antialiasing)
            p.setPen(QPen(Qt.black, 3.0))
            p.drawPoint(x, y)

            self.update()

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.pressed = True

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressed = False

        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setBrush(Qt.gray)
        p.drawRect(self.rect())

        p.setBrush(Qt.white)
        p.drawRect(self.image.rect())
        p.drawImage(0, 0, self.image)

        super().paintEvent(event)