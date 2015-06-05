#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from abstract_instrument import AbstractInstrument
from PySide.QtCore import Qt
from PySide.QtGui import *


class PencilInstrument(AbstractInstrument):
    def mousePressEvent(self, event, canvas):
        if event.buttons() == Qt.LeftButton or event.buttons() == Qt.RightButton:
            self.mStartPoint = event.pos()
            self.mEndPoint = event.pos()
            canvas.setIsPaint(True)
            self.makeUndoCommand(canvas)

    def mouseMoveEvent(self, event, canvas):
        if canvas.isPaint():
            self.mEndPoint = event.pos()

            if event.buttons() == Qt.LeftButton:
                self.paint(canvas, False)
            elif event.buttons() == Qt.RightButton:
                self.paint(canvas, True)

            self.mStartPoint = event.pos()

    def mouseReleaseEvent(self, event, canvas):
        if canvas.isPaint():
            self.mEndPoint = event.pos()

            if event.buttons() == Qt.LeftButton:
                self.paint(canvas, False)
            elif event.buttons() == Qt.RightButton:
                self.paint(canvas, True)

            canvas.setIsPaint(False)

    def paint(self, canvas, isSecondaryColor = False, additionalFlag = False):
        painter = QPainter(canvas.getImage())
        pen = QPen()
        # TODO: брать найстройки из класса-синглетона
        # pen.setWidth(DataSingleton::Instance()->getPenSize() * canvas.getZoomFactor())
        pen.setWidthF(2.0)
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        if isSecondaryColor:
            # pen.setBrush(DataSingleton::Instance()->getSecondaryColor())
            pen.setBrush(Qt.white)
        else:
            # pen.setBrush(DataSingleton::Instance()->getPrimaryColor())
            pen.setBrush(Qt.black)

        painter.setPen(pen)

        if self.mStartPoint != self.mEndPoint:
            painter.drawLine(self.mStartPoint, self.mEndPoint)

        if self.mStartPoint == self.mEndPoint:
            painter.drawPoint(self.mStartPoint)

        canvas.setEdited(True)

        painter.end()
        canvas.update()