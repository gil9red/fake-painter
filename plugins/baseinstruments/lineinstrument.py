#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from abstractinstrument import AbstractInstrument
from PySide.QtGui import *
from PySide.QtCore import *


class LineInstrument(AbstractInstrument):
    def __init__(self):
        self.__icon = QIcon('plugins/baseinstruments/icons/line.png')

    def name(self):
        return 'Line Instrument'

    def description(self):
        return 'Line Instrument'

    def icon(self):
        return self.__icon

    def mouse_press_event(self, event, canvas):
        self.mStartPoint = event.pos()
        self.mEndPoint = event.pos()
        self.mImageCopy = canvas.getImage()
        canvas.setIsPaint(True)
        self.make_undo_command(canvas)

    def mouse_move_event(self, event, canvas):
        if canvas.isPaint():
            self.mEndPoint = event.pos()
            canvas.setImage(self.mImageCopy.copy())

            if event.buttons() == Qt.LeftButton:
                self.paint(canvas, False)
            elif event.buttons() == Qt.RightButton:
                self.paint(canvas, True)

    def mouse_release_event(self, event, canvas):
        if canvas.isPaint():
            canvas.setIsPaint(False)

    def paint(self, canvas, is_secondary_color=False, additional_flag=False):
        painter = QPainter(canvas.getImage())
        pen = QPen()
        # TODO: брать найстройки из класса-синглетона
        # pen.setWidth(DataSingleton::Instance()->getPenSize() * canvas.getZoomFactor())
        pen.setWidthF(2.0)
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        # TODO: проработать этот момент -- у rect'а может быть
        # заливка каким-то цветом и нужно определить что будет закрашивать
        # левый и правый клики -- Pen или Brush
        if is_secondary_color:
            # pen.setBrush(DataSingleton::Instance()->getSecondaryColor())
            pen.setBrush(Qt.white)
        else:
            # pen.setBrush(DataSingleton::Instance()->getPrimaryColor())
            pen.setBrush(Qt.black)

        painter.setPen(pen)

        painter.drawLine(self.mStartPoint, self.mEndPoint)

        painter.end()

        canvas.setEdited(True)
        canvas.update()
