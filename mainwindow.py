#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

from mainwindow_ui import Ui_MainWindow
from PySide.QtGui import *
from PySide.QtCore import *

from pluginloader import PluginLoader
from canvas import Canvas


class MainWindow(QMainWindow, QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.canvas = Canvas()
        # self.setCentralWidget(self.canvas)

        scrollArea = QScrollArea()
        scrollArea.setWidget(self.canvas)
        # scrollArea.setWidgetResizable(True)
        scrollArea.setBackgroundRole(QPalette.Dark)

        self.ui.tabWidget.addTab(scrollArea, "untitled")

        # self.ui.scrollArea.setWidget(self.canvas)
        # self.ui.scrollArea.setBackgroundRole(QPalette.Dark)

        self.mUndoStackGroup = QUndoGroup(self)
        self.mUndoStackGroup.addStack(self.canvas.getUndoStack())
        self.mUndoStackGroup.setActiveStack(self.canvas.getUndoStack())

        self.mUndoStackGroup.canUndoChanged.connect(self.canUndoChanged)
        self.mUndoStackGroup.canRedoChanged.connect(self.canRedoChanged)

        self.canUndoChanged(self.mUndoStackGroup.canUndo())
        self.canRedoChanged(self.mUndoStackGroup.canRedo())

        self.ui.actionUndo.triggered.connect(self.mUndoStackGroup.undo)
        self.ui.actionRedo.triggered.connect(self.mUndoStackGroup.redo)


        loader = PluginLoader()
        loader.load('plugins')

        self.read_settings()

    def canUndoChanged(self, enabled):
        self.ui.actionUndo.setEnabled(enabled)

    def canRedoChanged(self, enabled):
        self.ui.actionRedo.setEnabled(enabled)

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