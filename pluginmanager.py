#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from pluginmanager_ui import Ui_PluginManager
from PySide.QtGui import *
from PySide.QtCore import *
from pluginmodel import PluginModel
from pluginsloader import PluginsLoader


class PluginManager(QDialog, QObject):
    def __init__(self, data_singleton, parent=None):
        super().__init__(parent)

        self.ui = Ui_PluginManager()
        self.ui.setupUi(self)

        self.data_singleton = data_singleton

        self.model = PluginModel(data_singleton)
        self.ui.view.setModel(self.model)

        self.ui.view.clicked.connect(self.clicked)

    def clicked(self, index):
        plugin = self.model.get(index)

        # TODO: использовать шаблоны
        text = plugin.name() + "\n" + plugin.version() + "\n" + plugin.description()
        self.ui.description.setText(text)

    def accept(self, *args, **kwargs):
        # Список отключенных плагинов
        new_disabled_plugins = []

        # Список включенных плагинов
        new_enabled_plugins = []

        for row in range(self.model.rowCount()):
            plugin = self.model.get_by_row(row)
            checked = self.model.is_checked(row)

            # Если снят флажок и плагин не является отключенным
            if not checked and plugin not in self.model.disabled_plugins.values():
                new_disabled_plugins.append(plugin)

            # Если поднят флаг и плагин был отключенным
            elif checked and plugin in self.model.disabled_plugins.values():
                new_enabled_plugins.append(plugin)

        loader = PluginsLoader(self.data_singleton)
        loader.disable_enabled_plugins(new_disabled_plugins)
        loader.enable_disabled_plugins(new_enabled_plugins)

        # self.datasingleton.image.history_depth = self.ui.sbHistoryDepth.value()
        # self.datasingleton.image.base_width = self.ui.sbWidth.value()
        # self.datasingleton.image.base_height = self.ui.sbHeight.value()
        #
        # self.datasingleton.mainWindow.write_settings()

        super().accept()
