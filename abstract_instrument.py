#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from abc import *


class AbstractInstrument(metaclass=ABCMeta):
    def __init__(self):
        self.mStartPoint = None
        self.mEndPoint = None
        self.mImageCopy = None

    @abstractmethod
    def mousePressEvent(self, event, canvas):
        pass

    @abstractmethod
    def mouseMoveEvent(self, event, canvas):
        pass

    @abstractmethod
    def mouseReleaseEvent(self, event, canvas):
        pass

    @abstractmethod
    def paint(self, canvas, isSecondaryColor = False, additionalFlag = False):
        pass

    def makeUndoCommand(self, canvas):
        """
        Creates UndoCommand & pushes it to UndoStack.
        Base realisation simply save all image to UndoStack
        """

        # TODO: передавать только canvas
        # TODO: раскомментировать
        # canvas.pushUndoCommand(UndoCommand(canvas.getImage(), canvas))