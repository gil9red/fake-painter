#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from iplugin import IPlugin
# from abstractfilter import AbstractFilter
from .negativefilter import NegativeFilter
from .grayscalefilter import GrayscaleFilter
from .swaprgbfilter import SwapRGBFilter

from PySide.QtGui import *
# from PySide.QtCore import *


class PluginBaseFilters(IPlugin):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton
        self.mw = data_singleton.mainWindow
        self.base_filter_action_group = None
        self.menu_filters = self.mw.ui.menuFilters
        self.filters = []

    def name(self):
        return 'Base Filters'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Base Filters'

    def initialize(self):
        # extension = '.py'
        #
        # # TODO: сделать такое же динамическое импортирование у baseinstruments
        # import os
        # cur_dir = os.path.dirname(__file__)
        # for file_name in os.listdir(cur_dir):
        #     if file_name != '__init__.py' and file_name.endswith(extension):
        #         modulename = file_name[: -len(extension)]
        #         # Попытаться импортировать модуль
        #         package = __import__(__package__ + "." + modulename)
        #         module = getattr(package, modulename)
        #
        #         for obj in dir(module):
        #             val = getattr(module, obj)
        #             if obj.endswith('Filter') and obj != 'AbstractFilter':
        #                 if issubclass(val, AbstractFilter):
        #                     print(val)
        #                     self.filters.append(val())
        # print()

        # for obj in AbstractFilter.__subclasses__():
        #     print(obj)
        #     self.filters.append(obj())

        # import os
        # cur_dir = os.path.dirname(__file__)
        # for f in os.listdir(cur_dir):
        #     print(f)
        # print()

        self.filters.append(NegativeFilter())
        self.filters.append(GrayscaleFilter())
        self.filters.append(SwapRGBFilter())

        self.base_filter_action_group = QActionGroup(self.menu_filters)
        self.base_filter_action_group.triggered.connect(lambda x: self.triggered_action_filter(x))

        for filter_ in self.filters:
            act = self.menu_filters.addAction(filter_.name())
            # TODO: objectName вида <class 'baseinstruments.rectangleinstrument.RectangleInstrument'>
            # кажется неудобным, может другое значение составлять
            act.setObjectName(str(type(filter_)))
            act.setToolTip(filter_.description())
            if filter_.icon():
                act.setIcon(filter_.icon())

            self.base_filter_action_group.addAction(act)
            self.data_singleton.action_filter_dict[act] = filter_

    def destroy(self):
        for act in self.data_singleton.action_filter_dict.keys():
            self.menu_filters.removeAction(act)

        self.filters.clear()
        self.data_singleton.action_filter_dict.clear()
        self.base_filter_action_group.deleteLater()
        self.base_filter_action_group = None

    def triggered_action_filter(self, action):
        filter_ = self.data_singleton.action_filter_dict[action]
        filter_.apply_filter(self.mw.get_current_canvas())
