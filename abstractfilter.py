#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from abc import ABCMeta, abstractproperty, abstractmethod
from undocommand import UndoCommand


# TODO: может и версию добавить?

class AbstractFilter(metaclass=ABCMeta):
    """Abstract class for implementing filters."""

    @abstractproperty
    def name(self):
        """Свойство должно возвращать имя фильтра"""

    @abstractproperty
    def description(self):
        """Свойство должно возвращать всплывающую подсказку к фильтру"""

    @abstractproperty
    def icon(self):
        """Свойство должно возвращать иконку фильтра"""

    @abstractmethod
    def apply_filter(self, canvas):
        """Функция вызывает воздействие на холст"""

    @staticmethod
    def make_undo_command(canvas):
        """Creates UndoCommand & pushes it to UndoStack.
        Base realisation simply save all image to UndoStack

        """

        canvas.push_undo_command(UndoCommand(canvas))
