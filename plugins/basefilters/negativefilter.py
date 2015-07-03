#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from abstractfilter import AbstractFilter


class NegativeFilter(AbstractFilter):
    # def __init__(self):
    #     self.__icon = QIcon('plugins/baseinstruments/icons/line.png')

    def name(self):
        return 'Negative Filter'

    def description(self):
        return 'Negative Filter'

    def icon(self):
        # return self.__icon
        return None

    def apply_filter(self, canvas):
        # TODO: проверять canvas на Nоne, логировать
        # TODO: реализовать
        # canvas.clearSelection();
        self.make_undo_command(canvas)

        canvas.getImage().invertPixels()
        canvas.setEdited(True)
        canvas.update()
