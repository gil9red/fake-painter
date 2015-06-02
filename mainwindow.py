#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mainwindow_ui import Ui_MainWindow
from PySide.QtGui import *
from PySide.QtCore import *

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

        self.read_settings()

    def read_settings(self):
        ini = QSettings('settings.ini')
        self.restoreGeometry(ini.value('MainWindow_Geometry'))
        self.restoreState(ini.value('MainWindow_State'))
        # self.ui.splitter.restoreState(ini.value('Splitter_State'))

    def write_settings(self):
        ini = QSettings('settings.ini')
        ini.setValue('MainWindow_State', self.saveState())
        ini.setValue('MainWindow_Geometry', self.saveGeometry())
        # ini.setValue('Splitter_State', self.ui.splitter.saveState())

    def closeEvent(self, *args, **kwargs):
        self.write_settings()

        super().closeEvent(*args, **kwargs)