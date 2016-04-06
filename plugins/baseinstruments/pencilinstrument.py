#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'

from abstractinstrument import AbstractInstrument
from PySide.QtGui import QIcon, QPainter, QPen
from PySide.QtCore import Qt


class PencilInstrument(AbstractInstrument):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton
        self.__icon = QIcon('plugins/baseinstruments/icons/pencil.png')

    def name(self):
        return 'Pencil Instrument'

    def description(self):
        return 'Pencil Instrument'

    def icon(self):
        return self.__icon

    def cursor(self):
        # TODO: support this
        pass

    def mouse_press_event(self, event, canvas):
        if event.buttons() == Qt.LeftButton or event.buttons() == Qt.RightButton:
            self._start_point = event.pos()
            self._end_point = event.pos()
            canvas.setIsPaint(True)
            self.make_undo_command(canvas)

    def mouse_move_event(self, event, canvas):
        if canvas.isPaint():
            self._end_point = event.pos()

            if event.buttons() == Qt.LeftButton:
                self.paint(canvas, False)
            elif event.buttons() == Qt.RightButton:
                self.paint(canvas, True)

            self._start_point = event.pos()

    def mouse_release_event(self, event, canvas):
        if canvas.isPaint():
            self._end_point = event.pos()

            if event.button() == Qt.LeftButton:
                self.paint(canvas, False)
            elif event.button() == Qt.RightButton:
                self.paint(canvas, True)

            canvas.setIsPaint(False)

    def paint(self, canvas, is_secondary_color=False, additional_flag=False):
        painter = QPainter(canvas.image)
        pen = QPen()
        # TODO: брать найстройки из класса-синглетона
        # pen.setWidth(DataSingleton::Instance()->getPenSize() * canvas.getZoomFactor())
        pen.setWidthF(2.0)
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        if is_secondary_color:
            pen.setBrush(self.data_singleton.secondary_color)
        else:
            pen.setBrush(self.data_singleton.primary_color)

        painter.setPen(pen)

        if self._start_point != self._end_point:
            painter.drawLine(self._start_point, self._end_point)

        if self._start_point == self._end_point:
            painter.drawPoint(self._start_point)

        painter.end()

        canvas.edited = True
        canvas.update()
