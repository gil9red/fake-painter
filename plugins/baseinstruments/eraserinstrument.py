#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from abstractinstrument import AbstractInstrument
from PySide.QtGui import QIcon


class EraserInstrument(AbstractInstrument):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton
        self._icon = QIcon('plugins/baseinstruments/icons/lastic.png')

    def name(self):
        return 'Eraser Instrument'

    def description(self):
        return 'Eraser Instrument'

    def icon(self):
        return self._icon

    def cursor(self):
        # TODO: support this
        pass

    def mouse_press_event(self, event, canvas):
        self._start_point = event.pos()
        self._end_point = event.pos()
        canvas.setIsPaint(True)

        self.make_undo_command(canvas)

    def mouse_move_event(self, event, canvas):
        if canvas.isPaint():
            self._end_point = event.pos()
            self.paint(canvas)
            self._start_point = event.pos()

    def mouse_release_event(self, event, canvas):
        if canvas.isPaint():
            self._end_point = event.pos()
            self.paint(canvas)
            canvas.setIsPaint(False)

    def paint(self, canvas, is_secondary_color=False, additional_flag=False):
        # TODO: поддержка разных размеров
        # TODO: поддержка очищения прозрачными пикселями
        x, y = self._start_point.x(), self._start_point.y()
        erase_color = self.data_singleton.secondary_color.rgba()

        for i in range(-20, 20):
            for j in range(-20, 20):
                check_x = canvas.image.width() > x + i >= 0
                check_y = canvas.image.height() > y + j >= 0
                if check_x and check_y:
                    canvas.image.setPixel(x + i, y + j, erase_color)

        canvas.edited = True
        canvas.update()
