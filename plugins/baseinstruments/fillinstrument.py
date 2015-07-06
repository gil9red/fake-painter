#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from abstractinstrument import AbstractInstrument
from PySide.QtGui import *
from PySide.QtCore import *


class FillInstrument(AbstractInstrument):
    def __init__(self):
        self._icon = QIcon('plugins/baseinstruments/icons/fill.png')

    def name(self):
        return 'Fill Instrument'

    def description(self):
        return 'Fill Instrument'

    def icon(self):
        return self._icon

    def mouse_press_event(self, event, canvas):
        if event.buttons() == Qt.LeftButton or event.buttons() == Qt.RightButton:
            self.mStartPoint = event.pos()
            self.mEndPoint = event.pos()
            canvas.setIsPaint(True)
            self.make_undo_command(canvas)

    def mouse_move_event(self, event, canvas):
        pass

    def mouse_release_event(self, event, canvas):
        if canvas.isPaint():
            if event.button() == Qt.LeftButton:
                self.paint(canvas, False)
            elif event.button() == Qt.RightButton:
                self.paint(canvas, True)

            canvas.setIsPaint(False)

    def paint(self, canvas, is_secondary_color=False, additional_flag=False):
        # TODO: настройки брать из синглетона
        if is_secondary_color:
            # switch_color = DataSingleton::Instance()->getSecondaryColor()
            switch_color = QColor(Qt.white)
        else:
            # switch_color = DataSingleton::Instance()->getPrimaryColor()
            switch_color = QColor(Qt.black)

        x, y = self.mStartPoint.x(), self.mStartPoint.y()

        pixel = canvas.image.pixel(x, y)
        old_color = QColor(pixel)

        if switch_color != old_color:
            self.fill_recurs(x, y,
                             switch_color.rgb(), old_color.rgb(),
                             canvas.image)

        self.fill_recurs(x, y, switch_color.rgb(), old_color.rgb(), canvas.image)

        canvas.setEdited(True)
        canvas.update()

    def fill_recurs(self, x, y, switch_color, old_color, temp_image):
        temp_x, left_x = x, 0

        while True:
            if temp_image.pixel(temp_x, y) != old_color:
                break

            temp_image.setPixel(temp_x, y, switch_color)
            if temp_x > 0:
                temp_x -= 1
                left_x = temp_x
            else:
                break

        right_x = 0
        temp_x = x + 1

        while True:
            if temp_image.pixel(temp_x, y) != old_color:
                break

            temp_image.setPixel(temp_x, y, switch_color)
            if temp_x < temp_image.width() - 1:
                temp_x += 1
                right_x = temp_x
            else:
                break

        for x_ in range(left_x + 1, right_x):
            if y < 1 or y >= temp_image.height() - 1:
                break

            if right_x > temp_image.width():
                break

            current_color = temp_image.pixel(x_, y - 1)
            if current_color == old_color and current_color != switch_color:
                self.fill_recurs(x_, y - 1, switch_color, old_color, temp_image)

            current_color = temp_image.pixel(x_, y + 1)
            if current_color == old_color and current_color != switch_color:
                self.fill_recurs(x_, y + 1, switch_color, old_color, temp_image)
