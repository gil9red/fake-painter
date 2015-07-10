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
import os


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

        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSaveAs.triggered.connect(self.save_as)
        self.ui.actionNew.triggered.connect(self.new_tab)
        self.ui.actionOpen.triggered.connect(self.open)

        self.ui.actionSettings.triggered.connect(self.show_settings)

        self.ui.actionPlugin_Manager.triggered.connect(self.show_plugin_manager)

        self.ui.tabWidget.currentChanged.connect(self.activate_tab)
        self.ui.tabWidget.currentChanged.connect(self.send_tab_changed)

        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.update_states()

    send_cursor_pos = Signal(int, int)
    send_new_image_size = Signal(int, int)
    send_tab_changed = Signal(int)

    def load_plugins(self):
        # TODO: проверить импортирование пакетов пакетов
        loader = PluginsLoader(self.data_singleton)
        loader.enableOutput = True
        # TODO: список папок плагинов доставать из синглетона
        loader.load(['plugins'])

        # TODO: rem
        print('Plugins:')
        for plugin in loader.plugins():
            print('  ', plugin)
        print()

    def update_states(self):
        if self.ui.tabWidget.count() == 0:
            self.setWindowTitle('Empty' + ' - ' + self.data_singleton.PROGRAM_NAME)
        else:
            canvas = self.get_current_canvas()
            file_name = canvas.get_file_name()

            title = self.data_singleton.UNTITLED if file_name is None else file_name
            tab_title = title

            if canvas.edited:
                title += '[*]'
                tab_title += '*'

            self.setWindowTitle(title + ' - ' + self.data_singleton.PROGRAM_NAME)

            index = self.ui.tabWidget.currentIndex()
            self.ui.tabWidget.setTabText(index, tab_title)

            self.setWindowModified(canvas.edited)

    def close_tab(self, index):
        canvas = self.get_canvas(index)
        if canvas.edited:
            reply = QMessageBox.warning(self,
                                        "Closing Tab...",
                                        "File has been modified\n"
                                        "Do you want to save changes?",
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                        QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                self.save(canvas)
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

        canvas.send_cursor_pos.connect(self.send_cursor_pos)
        canvas.send_new_image_size.connect(self.send_new_image_size)
        canvas.send_change_edited.connect(self.update_states)

        scroll_area = QScrollArea()
        scroll_area.setWidget(canvas)
        scroll_area.setBackgroundRole(QPalette.Dark)

        file_name = canvas.get_file_name()
        title = self.data_singleton.UNTITLED if file_name is None else file_name
        self.ui.tabWidget.addTab(scroll_area, title)

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
        self.mUndoStackGroup.setActiveStack(canvas.getUndoStack())

        self.send_new_image_size.emit(canvas.width(), canvas.height())

        self.update_states()

    def save(self, canvas_=None):
        try:
            # Если canvas_ не указан, берем текущий
            canvas = self.get_current_canvas() if canvas_ is None else canvas_
            if canvas is not None:
                # Если у холста есть файл, сохраняем в него, иначе вызываем "сохранить как"
                if canvas.file_path is None:
                    self.save_as()
                else:
                    canvas.save()

        except Exception as e:
            QMessageBox.warning(self, 'Warning', str(e))

        self.update_states()

    def save_as(self):
        canvas = self.get_current_canvas()
        if canvas is None:
            return

        # Список строк с поддерживаемыми форматами изображений
        formats = [str(x) for x in QImageWriter.supportedImageFormats()]

        # Описываем как фильтры диалога
        filters = ["{} ( *.{} )".format(x.upper(), x) for x in formats]

        file_name = canvas.get_file_name()
        if file_name is None:
            file_name = os.path.join(QDir.homePath(), self.data_singleton.UNTITLED)

        # TODO: суффикс по умолчанию -- png
        # Получим путь к файлу
        file_name = QFileDialog.getSaveFileName(self, None, file_name, '\n'.join(filters))[0]
        if file_name:
            try:
                canvas.save(file_name)
            except Exception as e:
                QMessageBox.warning(self, 'Warning', str(e))

        self.update_states()

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
                canvas = self.get_current_canvas()
                if canvas is not None:
                    canvas.load(file_name)
                    self.update_states()

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

                # TODO: синглетон должен сам грузить свои настройки, еще до загрузки mainwindow
                # self.data_singleton.from_serialize(data['Settings'])
        except Exception as e:
            print(e)

    def write_settings(self):
        # TODO: для ini есть модуль ConfigParser

        try:
            import json
            with open(self.data_singleton.settings_path, 'w') as f:
                data = {
                    'MainWindow': {
                        'state': str(self.saveState().toHex()),
                        'geometry': str(self.saveGeometry().toHex()),
                    },

                    # TODO: вызывать у синглетона функцию
                    'Settings': self.data_singleton.to_serialize(),
                }

                json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)

    def closeEvent(self, *args, **kwargs):
        self.write_settings()

        # Закрывать вкладки будем с правого края
        for i in reversed(range(self.ui.tabWidget.count())):
            self.close_tab(i)

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
