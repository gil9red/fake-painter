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

        self.mUndoStackGroup = QUndoGroup(self)

        self.mUndoStackGroup.canUndoChanged.connect(self.canUndoChanged)
        self.mUndoStackGroup.canRedoChanged.connect(self.canRedoChanged)

        self.canUndoChanged(self.mUndoStackGroup.canUndo())
        self.canRedoChanged(self.mUndoStackGroup.canRedo())

        self.ui.actionUndo.triggered.connect(self.mUndoStackGroup.undo)
        self.ui.actionRedo.triggered.connect(self.mUndoStackGroup.redo)

        # self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSaveAs.triggered.connect(self.save_as)
        self.ui.actionNew.triggered.connect(self.new_tab)
        self.ui.actionOpen.triggered.connect(self.open)

        # TODO: Добавить в виде плагина
        # self.ui.actionPrint

        self.ui.tabWidget.currentChanged.connect(self.activate_tab)
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        # loader = PluginLoader()
        # loader.load('plugins')

        self.read_settings()

        # TODO: удалить, пусть по умолчанию редактор пустой
        self.new_tab()

        self.updateStates()

    def updateStates(self):
        title = 'Empty'

        if self.ui.tabWidget.count() > 0:
            canvas = self.get_current_canvas()
            title = canvas.getFileName()

        # TODO: названия проги хранить в синглетоне, и оттуда брать
        self.setWindowTitle(title + " - fake-painter")


    def close_tab(self, index):
        canvas = self.get_canvas(index)
        if canvas.getEdited():
            reply = QMessageBox.warning(self,
                                      "Closing Tab...",
                                      "File has been modified\n"
                                      "Do you want to save changes?",
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                      QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                canvas.save()
            elif reply == QMessageBox.Cancel:
                return

        self.mUndoStackGroup.removeStack(canvas.getUndoStack())

        tab = self.ui.tabWidget.widget(index)
        self.ui.tabWidget.removeTab(index)
        tab.deleteLater()

        self.updateStates()

    def new_tab(self):
        canvas = Canvas()
        self.mUndoStackGroup.addStack(canvas.getUndoStack())

        scroll_area = QScrollArea()
        scroll_area.setWidget(canvas)
        scroll_area.setBackgroundRole(QPalette.Dark)

        self.ui.tabWidget.addTab(scroll_area, canvas.getFileName())

        self.updateStates()

    def activate_tab(self, index):
        if index == -1:
            return

        # # TODO: проверить, мне кажется при этом слоте так и так
        # # вкладка Index будет текущей
        # self.ui.tabWidget.setCurrentIndex(index)

        # TODO: реализовать
        # QSize size = getCurrentImageArea()->getImage()->size();
        # mSizeLabel->setText(QString("%1 x %2").arg(size.width()).arg(size.height()));

        canvas = self.get_current_canvas()
        self.mUndoStackGroup.setActiveStack(canvas.getUndoStack())

        self.updateStates()


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
                self.get_current_canvas().save(file_name)
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
                self.get_current_canvas().load(file_name)
            except Exception as e:
                QMessageBox.warning(self, 'Внимание', str(e))

    def canUndoChanged(self, enabled):
        self.ui.actionUndo.setEnabled(enabled)

    def get_canvas(self, index):
        if index < 0 or index >= self.ui.tabWidget.count():
            return None

        tab = self.ui.tabWidget.widget(index)
        return tab.widget()

    def get_current_canvas(self):
        index = self.ui.tabWidget.currentIndex()
        if index != -1:
            return self.get_canvas(index)

    def canRedoChanged(self, enabled):
        self.ui.actionRedo.setEnabled(enabled)

    def read_settings(self):
        ini = QSettings('settings.ini')
        self.restoreGeometry(ini.value('MainWindow_Geometry'))
        self.restoreState(ini.value('MainWindow_State'))

    def write_settings(self):
        ini = QSettings('settings.ini')
        ini.setValue('MainWindow_State', self.saveState())
        ini.setValue('MainWindow_Geometry', self.saveGeometry())

    def closeEvent(self, *args, **kwargs):
        self.write_settings()

        # reply = QtGui.QMessageBox.question(self, 'Message',
        #     "Are you sure to quit?", QtGui.QMessageBox.Yes |
        #     QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        #
        # if reply == QtGui.QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()

        super().closeEvent(*args, **kwargs)