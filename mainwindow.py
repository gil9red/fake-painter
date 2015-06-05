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

        self.mUndoStackGroup.setActiveStack(self.canvas.getUndoStack())

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
        # TODO: сделать, в оригинальном коде называлось enableActions
        # self.ui.tabWidget.currentChanged.connect(self.update_states)
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        loader = PluginLoader()
        loader.load('plugins')

        self.read_settings()

# void MainWindow::closeTab(int index)
# {
#     ImageArea *ia = getImageAreaByIndex(index);
#     if(ia->getEdited())
#     {
#         int ans = QMessageBox::warning(this, tr("Closing Tab..."),
#                                        tr("File has been modified\nDo you want to save changes?"),
#                                        QMessageBox::Yes | QMessageBox::Default,
#                                        QMessageBox::No, QMessageBox::Cancel | QMessageBox::Escape);
#         switch(ans)
#         {
#         case QMessageBox::Yes:
#             ia->save();
#             break;
#         case QMessageBox::Cancel:
#             return;
#         }
#     }
#     mUndoStackGroup->removeStack(ia->getUndoStack()); //for safety
#     QWidget *wid = mTabWidget->widget(index);
#     mTabWidget->removeTab(index);
#     delete wid;
#     if (mTabWidget->count() == 0)
#     {
#         setWindowTitle("Empty - EasyPaint");
#     }
# }

    def new_tab(self):
        canvas = Canvas()
        self.mUndoStackGroup.addStack(canvas.getUndoStack())

        scroll_area = QScrollArea()
        scroll_area.setWidget(canvas)
        scroll_area.setBackgroundRole(QPalette.Dark)

        self.ui.tabWidget.addTab(scroll_area, "untitled")

    def activate_tab(self, index):
        if index == -1:
            return

        # TODO: проверить, мне кажется при этом слоте так и так
        # вкладка Index будет текущей
        self.ui.tabWidget.setCurrentIndex(index)

        # TODO: реализовать
        # QSize size = getCurrentImageArea()->getImage()->size();
        # mSizeLabel->setText(QString("%1 x %2").arg(size.width()).arg(size.height()));

        canvas = self.currentCanvas()

        if not canvas.getFileName():
            self.setWindowTitle(canvas.getFileName() + " - fake-painter")
        else:
            self.setWindowTitle("Untitled Image" + " - EasyPaint")

        self.mUndoStackGroup.setActiveStack(canvas.getUndoStack())


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