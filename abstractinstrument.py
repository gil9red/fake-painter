#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'

from abc import *
from undocommand import UndoCommand


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
    def paint(self, canvas, is_secondary_color=False, additional_flag=False):
        pass

    def makeUndoCommand(self, canvas):
        """
        Creates UndoCommand & pushes it to UndoStack.
        Base realisation simply save all image to UndoStack
        """

        canvas.pushUndoCommand(UndoCommand(canvas))
