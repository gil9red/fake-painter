#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from iplugin import IPlugin
from PySide.QtGui import QPrinter, QPrintDialog, QDialog, QPainter


class PluginPrinter(IPlugin):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton

        self.mw = self.data_singleton.mainWindow
        self.actionPrint = None
        self.actionSep = None

    def name(self):
        return 'Printer'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Printer'

    def initialize(self):
        self.actionPrint = self.mw.ui.menuFile.addAction('Print')
        self.mw.ui.menuFile.insertAction(self.mw.ui.actionQuit, self.actionPrint)
        self.actionSep = self.mw.ui.menuFile.insertSeparator(self.mw.ui.actionQuit)

        self.actionPrint.triggered.connect(lambda: self.print_())

    def destroy(self):
        self.mw.ui.menuFile.removeAction(self.actionPrint)
        self.mw.ui.menuFile.removeAction(self.actionSep)

        self.actionPrint = None
        self.actionSep = None

    def print_(self):
        canvas = self.mw.get_current_canvas()
        if not canvas:
            return

        printer = QPrinter()
        dlg = QPrintDialog(printer, self.mw)
        if dlg.exec_() == QDialog.Accepted:
            painter = QPainter(printer)
            painter.drawImage(0, 0, canvas.image)
            painter.end()
