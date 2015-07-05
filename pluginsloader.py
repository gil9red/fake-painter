#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Eugeniy Ilin (aka Jenyay) <jenyay.ilin@gmail.com>
# Copyright: 2010, Eugeniy Ilin (aka Jenyay)
#
# Author: Ilya Petrash (aka gil9red) <ip1992@inbox.ru>
# Copyright (c) 2015 Ilya Petrash
#
# License: GPL3
#    This package is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This package is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this package; if not, see .
#
# On Debian systems, the complete text of the GNU General
# Public License can be found in 'http://www.gnu.org/licenses/gpl.html'.


__author__ = 'ipetrash'


import os
import os.path
import sys

from iplugin import IPlugin


class PluginsLoader:
    """Класс для загрузки плагинов"""

    def __init__(self, data_singleton):
        self.data_singleton = data_singleton

        # Словарь с загруженными плагинами
        # Ключ - имя плагина
        # Значение - экземпляр плагина
        self._plugins = {}

        # Словарь с плагинами, которые были отключены пользователем
        # Ключ - имя плагина
        # Значение - экземпляр плагина
        self._disabled_plugins = {}

        # Пути, где ищутся плагины
        self._dir_list = []

        # Имя классов плагинов должно начинаться с "Plugin"
        self._pluginsStartName = "Plugin"

        # Установить в False, если не нужно выводить ошибки(например, в тестах)
        self.enableOutput = True

    def _print(self, text):
        if self.enableOutput:
            print(text)

    @property
    def disabled_plugins(self):
        """Возвращает список отключенных плагинов"""

        return self._disabled_plugins

    def update_disable_list(self):
        """
        Обновление состояния плагинов. Одни отключить, другие включить
        """

        # Пройтись по включенным плагинам и отключить те,
        # что попали в черный список
        self._disable_enabled_plugins(self.data_singleton.disabled_plugins)

        # Пройтись по отключенным плагинам и включить те,
        # что не попали в "черный список"
        self._enable_disabled_plugins(self.data_singleton.disabled_plugins)

    def _disable_enabled_plugins(self, disable_list):
        """Отключить загруженные плагины, попавшие в "черный список" (disableList)"""

        for plugin_name in disable_list:
            if plugin_name in self._plugins.keys():
                self._plugins[plugin_name].destroy()

                assert plugin_name not in self._disabled_plugins
                self._disabled_plugins[plugin_name] = self._plugins[plugin_name]
                del self._plugins[plugin_name]

    def _enable_disabled_plugins(self, disable_list):
        """Включить отключенные плагины, если их больше нет в "черном списке"""

        for plugin in self._disabled_plugins.values():
            if plugin.name not in disable_list:
                plugin.initialize()

                assert plugin.name not in self._plugins
                self._plugins[plugin.name] = plugin

                del self._disabled_plugins[plugin.name]

    def load(self, dir_list):
        """Загрузить плагины из указанных директорий.
        Каждый вызов метода load() добавляет плагины в список загруженных плагинов, не очищая его
        dir_list - список директорий, где могут располагаться плагины. Каждый плагин расположен в своей поддиректории

        """

        assert dir_list is not None

        for currentDir in dir_list:
            if os.path.exists(currentDir):
                dir_packets = sorted(os.listdir(currentDir))

                # Добавить путь до currentDir в sys.path
                full_path = os.path.abspath(currentDir)

                # TODO: странное место
                syspath = [item for item in sys.path]

                if full_path not in syspath:
                    sys.path.insert(0, full_path)

                # Все поддиректории попытаемся открыть как пакеты
                self._import_modules(currentDir, dir_packets)

    def clear(self):
        """Уничтожить все загруженные плагины"""

        map(lambda plugin: plugin.destroy(), self._plugins.values())
        self._plugins = {}

    def _import_modules(self, base_dir, dir_packages_list):
        """Попытаться импортировать пакеты
        baseDir - директория, где расположены пакеты
        dirPackagesList - список директорий(только имена директорий), возможно являющихся пакетами

        """

        assert dir_packages_list is not None

        for packageName in dir_packages_list:
            if packageName == '__pycache__':
                continue

            package_path = os.path.join(base_dir, packageName)

            # TODO: если проверять на файл, то можно импортировать одиночные модули
            # Проверить, что это директория
            if os.path.isdir(package_path):
                # Список строк, описывающий возникшие ошибки во время импортирования
                # Выводятся только если не удалось импортировать ни одного модуля
                errors = []

                # Количество загруженных плагинов до импорта нового
                old_plugins_count = len(self._plugins) + len(self._disabled_plugins)

                # Переберем все файлы внутри packagePath
                # и попытаемся их импортировать
                for fileName in sorted(os.listdir(package_path)):
                    module = self._import_single_module(packageName, fileName)
                    if module is not None:
                        self._load_plugin(module)

                    # try:
                    #     module = self._import_single_module(packageName, fileName)
                    #     print('module=', module) # TODO: rem
                    #     if module is not None:
                    #         self.__load_plugin(module)
                    # except BaseException as e:
                    #     errors.append("*** Plugin {package} loading error ***\n"
                    #                   "{package}/{fileName}\n"
                    #                   "{error}".format(package=packageName,
                    #                                    fileName=fileName,
                    #                                    error=str(e)))

                # Проверим, удалось ли загрузить плагин
                new_plugins_count = len(self._plugins) + len(self._disabled_plugins)

                # Вывод ошибок, если ни одного плагина из пакета не удалось
                # импортировать
                if new_plugins_count == old_plugins_count and len(errors) != 0:
                    self._print(u"\n\n".join(errors))
                    self._print(u"**********\n")

    @staticmethod
    def _import_single_module(package_name, file_name):
        """Импортировать один модуль по имени пакета и файла с модулем"""

        # TODO: проверить импортирование таких модулей: '.pyс' или '.pyo'
        # Модуль может загружаться из файлов с расширением '.pyс' или '.pyo', даже если нет файла
        # с расширением '.py'. Это может пригодиться в тех случаях, когда вы не хотите распространять исходный код.

        extension = ".py"
        result = None

        # Проверим, что файл может быть модулем
        if file_name.endswith(extension) and file_name != "__init__.py":
            module_name = file_name[: -len(extension)]
            # Попытаться импортировать модуль
            package = __import__(package_name + "." + module_name)
            result = getattr(package, module_name)

        return result

    def _load_plugin(self, module):
        """Найти классы плагинов и создать их экземпляры"""

        assert module is not None

        # Перебираем список объектов в модуле
        for name in dir(module):
            self._create_object(module,
                                name,
                                self.data_singleton.disabled_plugins)

    def _create_object(self, module, name, disabled_plugins):
        """Попытаться загрузить класс, возможно, это плагин

        module - модуль, откуда загружается класс
        name - имя класса потенциального плагина

        """

        if name.startswith(self._pluginsStartName):
            obj = getattr(module, name)
            if obj not in IPlugin.__subclasses__():
                return

            # if obj == Plugin or not issubclass(obj, Plugin):
            #     return

            # Создаем плагин, и в его конструктор передаем datasingleton
            plugin = obj(self.data_singleton)
            if not self._is_new_plugin(plugin.name):
                return

            if plugin.name not in disabled_plugins:
                plugin.initialize()
                self._plugins[plugin.name] = plugin
            else:
                self._disabled_plugins[plugin.name] = plugin

    def _is_new_plugin(self, plugin_name):
        """Проверка того, что плагин с таким именем еще не был загружен
        plugin_name - плагин, который надо проверить

        """
        return(plugin_name not in self._plugins and
               plugin_name not in self._disabled_plugins)

    def plugins(self):
        return self._plugins.values()
