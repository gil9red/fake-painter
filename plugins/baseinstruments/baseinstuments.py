#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from iplugin import IPlugin
from .lineinstrument import LineInstrument
from .pencilinstrument import PencilInstrument
from .rectangleinstrument import RectangleInstrument
from .eraserinstrument import EraserInstrument
from .fillinstrument import FillInstrument

from PySide.QtGui import *
from PySide.QtCore import *

# TODO: добавить автоматический поиск плагинов
# TODO: rem import *

class PluginBaseInstruments(IPlugin):
    def __init__(self, data_singleton):
        self.data_singleton = data_singleton
        self.mw = self.data_singleton.mainWindow
        self.menu_instruments = None
        self.base_inst_tool_bar = None
        self.base_inst_action_group = None
        self.instruments = []

    def name(self):
        return 'Base Instruments'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Base Instruments'

    def initialize(self):
        self.instruments.append(EraserInstrument())
        self.instruments.append(PencilInstrument(self.data_singleton))
        self.instruments.append(LineInstrument(self.data_singleton))
        self.instruments.append(RectangleInstrument(self.data_singleton))
        self.instruments.append(FillInstrument(self.data_singleton))

        self.base_inst_tool_bar = self.mw.addToolBar(self.description())
        self.base_inst_tool_bar.setObjectName(self.name())
        self.base_inst_tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.base_inst_action_group = QActionGroup(self.base_inst_tool_bar)
        self.base_inst_action_group.setExclusive(True)
        self.base_inst_action_group.triggered.connect(lambda x: self.triggered_action_instrument(x))

        self.menu_instruments = self.mw.ui.menuInstruments

        for inst in self.instruments:
            act = self.base_inst_tool_bar.addAction(inst.name())
            # TODO: objectName вида <class 'baseinstruments.rectangleinstrument.RectangleInstrument'>
            # кажется неудобным, может другое значение составлять
            act.setObjectName(str(type(inst)))
            act.setToolTip(inst.description())
            if inst.icon():
                act.setIcon(inst.icon())
            act.setCheckable(True)

            self.base_inst_action_group.addAction(act)
            self.menu_instruments.addActions(self.base_inst_action_group.actions())
            self.data_singleton.action_inst_dict[act] = inst

    def destroy(self):
        self.instruments.clear()

        self.mw.removeToolBar(self.base_inst_tool_bar)

        # base_inst_tool_bar удалит и base_inst_action_group, и действия
        self.base_inst_tool_bar.deleteLater()
        self.base_inst_tool_bar = None
        self.base_inst_action_group = None

        self.data_singleton.action_inst_dict.clear()
        self.data_singleton.current_instrument = None

    def triggered_action_instrument(self, action):
        instrument = self.data_singleton.action_inst_dict[action]
        self.data_singleton.current_instrument = instrument
