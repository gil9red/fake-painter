#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'

from PySide.QtGui import *
from PySide.QtCore import *

from mainwindow_ui import Ui_MainWindow
from settings import Settings
from pluginmanager import PluginManager
from canvas import Canvas
from pluginsloader import PluginsLoader



class MainWindow(QMainWindow, QObject):
    def __init__(self, data_singleton, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.data_singleton = data_singleton

        self.mUndoStackGroup = QUndoGroup(self)

        self.mUndoStackGroup.canUndoChanged.connect(self.can_undo_changed)
        self.mUndoStackGroup.canRedoChanged.connect(self.can_redo_changed)

        self.can_undo_changed(self.mUndoStackGroup.canUndo())
        self.can_redo_changed(self.mUndoStackGroup.canRedo())

        self.ui.actionUndo.triggered.connect(self.mUndoStackGroup.undo)
        self.ui.actionRedo.triggered.connect(self.mUndoStackGroup.redo)

        # self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSaveAs.triggered.connect(self.save_as)
        self.ui.actionNew.triggered.connect(self.new_tab)
        self.ui.actionOpen.triggered.connect(self.open)

        self.ui.actionSettings.triggered.connect(self.show_settings)

        self.ui.actionPlugin_Manager.triggered.connect(self.show_plugin_manager)

        self.ui.tabWidget.currentChanged.connect(self.activate_tab)
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.update_states()

    send_cursor_pos = Signal(int, int)

    def load_plugins(self):
        # TODO: добавить application
        # TODO: проверить импортирование пакетов пакетов
        loader = PluginsLoader(self.data_singleton)
        loader.enableOutput = True
        # TODO: список папок плагинов доставать из синглетона
        loader.load(['plugins'])

        # TODO: rem
        print('Plugins:')
        for plugin in loader.plugins():
            print('  ', plugin)

    def update_states(self):
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

        self.update_states()

    def new_tab(self):
        canvas = Canvas(self.data_singleton)
        self.mUndoStackGroup.addStack(canvas.getUndoStack())

        scroll_area = QScrollArea()
        scroll_area.setWidget(canvas)
        scroll_area.setBackgroundRole(QPalette.Dark)

        self.ui.tabWidget.addTab(scroll_area, canvas.getFileName())

        self.update_states()

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

        canvas.send_cursor_pos.connect(self.send_cursor_pos)

        self.mUndoStackGroup.setActiveStack(canvas.getUndoStack())

        self.update_states()

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

    def show_settings(self):
        settings = Settings(self.data_singleton)
        settings.exec_()

    def show_plugin_manager(self):
        plugin_manager = PluginManager(self.data_singleton)
        plugin_manager.exec_()

    def can_undo_changed(self, enabled):
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

    def can_redo_changed(self, enabled):
        self.ui.actionRedo.setEnabled(enabled)

    def read_settings(self):
        try:
            import json
            with open(self.data_singleton.settings_path, 'r') as f:
                data = json.load(f)

                self.restoreGeometry(QByteArray.fromHex(data['MainWindow']['geometry']))
                self.restoreState(QByteArray.fromHex(data['MainWindow']['state']))

                self.data_singleton.from_serialize(data['Settings'])
        except Exception as e:
            print(e)

    def write_settings(self):
        try:
            import json
            with open(self.data_singleton.settings_path, 'w') as f:
                data = {
                    'MainWindow': {
                        'state': str(self.saveState().toHex()),
                        'geometry': str(self.saveGeometry().toHex()),
                    },

                    'Settings': self.data_singleton.to_serialize(),
                }

                json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)

    def closeEvent(self, *args, **kwargs):
        self.write_settings()

        # TODO: тут нужно закрывать все открытые вкладки

        # TODO: спрашивать о том уверенности пользователя нужно с учетом флажка
        # reply = QtGui.QMessageBox.question(self, 'Message',
        #     "Are you sure to quit?", QtGui.QMessageBox.Yes |
        #     QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        #
        # if reply == QtGui.QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()

        super().closeEvent(*args, **kwargs)
