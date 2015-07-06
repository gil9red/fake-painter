#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'

from abc import ABCMeta, abstractproperty, abstractmethod
from undocommand import UndoCommand


# TODO: может и версию добавить?
# TODO: добавить метод, возвращающий иконку инструмента

class AbstractInstrument(metaclass=ABCMeta):
    def __init__(self):
        self.mStartPoint = None
        self.mEndPoint = None
        self.mImageCopy = None

    @abstractproperty
    def name(self):
        """Свойство должно возвращать имя инструмента"""

    @abstractproperty
    def description(self):
        """Свойство должно возвращать всплывающую подсказку к инструменту"""

    @abstractproperty
    def icon(self):
        """Свойство должно возвращать иконку инструмента"""

    @abstractmethod
    def mouse_press_event(self, event, canvas):
        pass

    @abstractmethod
    def mouse_move_event(self, event, canvas):
        pass

    @abstractmethod
    def mouse_release_event(self, event, canvas):
        pass

    @abstractmethod
    def paint(self, canvas, is_secondary_color=False, additional_flag=False):
        pass

    @staticmethod
    def make_undo_command(canvas):
        """Creates UndoCommand & pushes it to UndoStack.
        Base realisation simply save all image to UndoStack

        """

        canvas.pushUndoCommand(UndoCommand(canvas))
