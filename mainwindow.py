#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mainwindow_ui import Ui_MainWindow
from PySide.QtGui import *

from pluginloader import PluginLoader

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loader = PluginLoader()
        loader.load('plugins')