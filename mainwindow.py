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

        # self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSaveAs.triggered.connect(self.save_as)

        self.ui.actionOpen.triggered.connect(self.open)

        # TODO: Добавить в виде плагина
        # self.ui.actionPrint

        loader = PluginLoader()
        loader.load('plugins')

        self.read_settings()

    # def save(self):
    #     print(self.currentCanvas())

    def save_as(self):
        # Список строк с поддерживаемыми форматами изображений
        formats = [str(x) for x in QImageWriter.supportedImageFormats()]

        # Описываем как фильтры диалога
        filters = ["{} ( *.{} )".format(x.upper(), x) for x in formats]

        # Получим путь к файлу
        file_name = QFileDialog.getSaveFileName(self, None, None, '\n'.join(filters))[0]
        if file_name:
            try:
                self.currentCanvas().save(file_name)
            except Exception as e:
                QMessageBox.warning(self, 'Внимание', str(e))

    def open(self):
        # Список строк с поддерживаемыми форматами изображений
        formats = [str(x) for x in QImageReader.supportedImageFormats()]

        # Описываем как фильтры диалога
        filters = 'Поддерживаемые форматы ('
        filters += ' '.join(["*.{}".format(x.lower()) for x in formats])
        filters += ')'

        # Получим путь к файлу
        file_name = QFileDialog.getOpenFileName(self, None, None, filters)[0]
        if file_name:
            try:
                self.currentCanvas().load(file_name)
            except Exception as e:
                QMessageBox.warning(self, 'Внимание', str(e))

    def canUndoChanged(self, enabled):
        self.ui.actionUndo.setEnabled(enabled)

    def currentCanvas(self):
        if self.ui.tabWidget.currentWidget():
            scroll_area = self.ui.tabWidget.currentWidget()
            return scroll_area.widget()

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