#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from PySide.QtGui import *


class UndoCommand(QUndoCommand):
    """
    Class which provides undo/redo actions
    """

    def __init__(self, canvas, parent=None):
        super().__init__(parent)

        self.mPrevImage = canvas.image.copy()
        self.mCurrImage = canvas.image.copy()
        self.canvas = canvas

    def undo(self):
        # TODO: проверить и реализовать clearSelection
        # self.canvas.clearSelection()
        self.mCurrImage = self.canvas.image.copy()
        self.canvas.image = self.mPrevImage
        self.canvas.update()
        # TODO: проверить и реализовать saveImageChanges
        # self.canvas.saveImageChanges()

    def redo(self):
        self.canvas.image = self.mCurrImage
        self.canvas.update()
        # TODO: проверить и реализовать saveImageChanges
        # self.canvas.saveImageChanges()
