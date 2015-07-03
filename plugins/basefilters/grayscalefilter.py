#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from abstractfilter import AbstractFilter
from PySide.QtGui import qGray, qAlpha, qRgba


class GrayscaleFilter(AbstractFilter):
    # def __init__(self):
    #     self.__icon = QIcon('plugins/baseinstruments/icons/line.png')

    def name(self):
        return 'Grayscale Filter'

    def description(self):
        return 'Grayscale Filter'

    def icon(self):
        # return self.__icon
        return None

    def apply_filter(self, canvas):
        # TODO: проверять canvas на Nоne, логировать
        # TODO: реализовать
        # canvas.clearSelection();
        self.make_undo_command(canvas)

        im = canvas.image

        for y in range(im.height()):
            for x in range(im.width()):
                pixel = im.pixel(x, y)
                gray = qGray(pixel)
                alpha = qAlpha(pixel)
                im.setPixel(x, y, qRgba(gray, gray, gray, alpha))

        canvas.setEdited(True)
        canvas.update()
