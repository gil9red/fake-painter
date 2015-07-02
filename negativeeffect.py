#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from abstracteffect import AbstractEffect
from PySide.QtGui import QImage


class NegativeEffect(AbstractEffect):
    # def __init__(self):
    #     self.__icon = QIcon('plugins/baseinstruments/icons/line.png')

    def name(self):
        return 'Negative Effect'

    def description(self):
        return 'Negative Effect'

    def icon(self):
        return self.__icon

    def apply_effect(self, canvas):
        # TODO: проверять canvas на Nоne, логировать
        # TODO: реализовать
        # canvas.clearSelection();
        self.make_undo_command(canvas)

        canvas.getImage().invertPixels(QImage.InvertRgb)
        canvas.setEdited(True)
        canvas.update()
