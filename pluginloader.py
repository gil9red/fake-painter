#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from importlib.machinery import SourceFileLoader
import glob
import os
import sys
from iplugin import IPlugin

class PluginLoader:
    def __init__(self):
        self.plugins = []

    def load(self, dir_name):
        sys.path.insert(0, dir_name)  # Добавляем папку плагинов в $PATH, чтобы __import__ мог их загрузить

        for f in glob.glob(dir_name + '/*.py'):
            name = os.path.basename(f)
            module = os.path.splitext(name)[0]  # имя без суффикса .py
            print('Found plugin', name)
            __import__(module)  # Импортируем исходник плагина

        print()

        # так как IPlugin произведен от object, мы используем __subclasses__,
        # чтобы найти все плагины, произведенные от этого класса
        for plugin in IPlugin.__subclasses__():
            print(plugin)
            p = plugin()  # Создаем экземпляр
            self.plugins.append(p)
            p.init()  # Вызываем событие загруки этого плагина

        return

    # def load(self, dir_name):
    #     """"""
    #
    #     for f in glob.glob(dir_name + '/*.py'):
    #         name = os.path.basename(f)
    #         module = SourceFileLoader(name, f).load_module()
    #         plugin = None
    #
    #         # Имя класса плагина должно совпадать с названием
    #         # модуля плагина
    #         for n in dir(module):
    #             if name.startswith(n.lower()):
    #                 obj = getattr(module, n)
    #                 plugin = obj()
    #                 break
    #
    #         print(plugin.name(), plugin.version())
    #         plugin.init()
    #
    #         self.plugins.append(plugin)

    # def