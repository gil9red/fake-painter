#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from abstractinstrument import AbstractInstrument
from PySide.QtGui import *
from PySide.QtCore import *


class EraserInstrument(AbstractInstrument):
    def __init__(self):
        self._icon = QIcon('plugins/baseinstruments/icons/lastic.png')
        self._transparent = QColor(Qt.transparent).rgba()

    def name(self):
        return 'Eraser Instrument'

    def description(self):
        return 'Eraser Instrument'

    def icon(self):
        return self._icon

    def mouse_press_event(self, event, canvas):
        self.mStartPoint = event.pos()
        self.mEndPoint = event.pos()
        canvas.setIsPaint(True)

        self.make_undo_command(canvas)

    def mouse_move_event(self, event, canvas):
        if canvas.isPaint():
            self.mEndPoint = event.pos()
            self.paint(canvas)
            self.mStartPoint = event.pos()

    def mouse_release_event(self, event, canvas):
        if canvas.isPaint():
            self.mEndPoint = event.pos()
            self.paint(canvas)
            canvas.setIsPaint(False)

    def paint(self, canvas, is_secondary_color=False, additional_flag=False):
        # TODO: рефакторинг
        # TODO: поддержка разных размеров
        x, y = self.mStartPoint.x(), self.mStartPoint.y()

        for i in range(-20, 20):
            for j in range(-20, 20):
                if x + i < canvas.image.width() and y + j < canvas.image.height() and x + i >= 0 and y + j >= 0:
                    canvas.image.setPixel(x + i, y + j, self._transparent)

        # painter = QPainter(canvas.image)
        # # TODO: оставлять после ластика ничего -- должен быть виден задний фон
        # # painter.setPen(QPen(Qt.transparent,
        # painter.setPen(QPen(Qt.white,
        #                     # TODO: брать найстройки из класса-синглетона
        #                     # DataSingleton::Instance()->getPenSize() * imageArea.getZoomFactor(),
        #                     2.0,
        #                     Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        #
        # if self.mStartPoint != self.mEndPoint:
        #     painter.drawLine(self.mStartPoint, self.mEndPoint)
        #
        # if self.mStartPoint == self.mEndPoint:
        #     painter.drawPoint(self.mStartPoint)
        #
        # painter.end()

        canvas.setEdited(True)
        canvas.update()
