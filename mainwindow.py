#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mainwindow_ui import Ui_MainWindow
from PySide.QtGui import *

from pluginloader import PluginLoader
from canvas import Canvas

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        loader = PluginLoader()
        loader.load('plugins')