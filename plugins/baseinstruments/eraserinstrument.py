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
        self.__icon = QIcon('plugins/baseinstruments/icons/lastic.png')

    def name(self):
        return 'Eraser Instrument'

    def description(self):
        return 'Eraser Instrument'

    def icon(self):
        return self.__icon

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
        painter = QPainter(canvas.image)
        # TODO: оставлять после ластика ничего -- должен быть виден задний фон
        # painter.setPen(QPen(Qt.transparent,
        painter.setPen(QPen(Qt.white,
                            # TODO: брать найстройки из класса-синглетона
                            # DataSingleton::Instance()->getPenSize() * imageArea.getZoomFactor(),
                            2.0,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        if self.mStartPoint != self.mEndPoint:
            painter.drawLine(self.mStartPoint, self.mEndPoint)

        if self.mStartPoint == self.mEndPoint:
            painter.drawPoint(self.mStartPoint)

        painter.end()

        canvas.setEdited(True)
        canvas.update()
