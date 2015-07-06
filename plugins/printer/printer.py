#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from iplugin import IPlugin
from PySide.QtGui import *


class PluginPrinter(IPlugin):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton

        self.actionPrint = None
        self.actionSep = None

    def name(self):
        return 'Printer'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Printer'

    def initialize(self):
        mw = self.data_singleton.mainWindow

        self.actionPrint = mw.ui.menuFile.addAction('Print')
        mw.ui.menuFile.insertAction(mw.ui.actionQuit, self.actionPrint)
        self.actionSep = mw.ui.menuFile.insertSeparator(mw.ui.actionQuit)

        self.actionPrint.triggered.connect(lambda: self.print_())

    def destroy(self):
        # TODO: поддержать
        pass

    def print_(self):
        mw = self.data_singleton.mainWindow
        canvas = mw.get_current_canvas()
        if not canvas:
            return

        printer = QPrinter()
        dlg = QPrintDialog(printer, mw)
        if dlg.exec_() == QDialog.Accepted:
            painter = QPainter(printer)
            painter.drawImage(0, 0, canvas.image)
            painter.end()
