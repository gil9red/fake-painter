#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


# TODO: плагин импортирует инструменты и возвращает их список

from iplugin import IPlugin
from .negativefilter import NegativeFilter

from PySide.QtGui import *
from PySide.QtCore import *


class PluginBaseFilters(IPlugin):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton
        self.filters = []

    def name(self):
        return 'Base Filters'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Base Filters'

    def initialize(self):
        self.filters.append(NegativeFilter())

        mw = self.data_singleton.mainWindow

        # base_inst_tool_bar = mw.addToolBar(self.description())
        # base_inst_tool_bar.setObjectName(self.name())
        # base_inst_tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        #
        # mw.base_inst_action_group = QActionGroup(base_inst_tool_bar)
        # mw.base_inst_action_group.setExclusive(True)
        # mw.base_inst_action_group.triggered.connect(lambda x: self.triggered_action_instrument(x))

        menu_filters = mw.ui.menuFilters

        mw.base_filter_action_group = QActionGroup(menu_filters)
        mw.base_filter_action_group.setExclusive(True)
        mw.base_filter_action_group.triggered.connect(lambda x: self.triggered_action_filter(x))

        for filter_ in self.filters:
            # act = base_inst_tool_bar.addAction(inst.icon(), inst.name())
            act = menu_filters.addAction(filter_.name())
            # TODO: objectName вида <class 'baseinstruments.rectangleinstrument.RectangleInstrument'>
            # кажется неудобным, может другое значение составлять
            act.setObjectName(str(type(filter_)))
            act.setToolTip(filter_.description())
            if filter_.icon():
                act.setIcon(filter_.icon())
            act.setCheckable(True)

            mw.base_filter_action_group.addAction(act)
            # menu_instruments.addActions(mw.base_inst_action_group.actions())
            self.data_singleton.action_filter_dict[act] = filter_

    def triggered_action_filter(self, action):
        mw = self.data_singleton.mainWindow

        filter_ = self.data_singleton.action_filter_dict[action]
        filter_.apply_filter(mw.get_current_canvas())

