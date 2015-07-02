#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


# TODO: плагин импортирует инструменты и возвращает их список

from iplugin import IPlugin
from .lineinstrument import LineInstrument
from .pencilinstrument import PencilInstrument
from .rectangleinstrument import RectangleInstrument

from PySide.QtGui import *
from PySide.QtCore import *


class PluginBaseInstruments(IPlugin):
    def __init__(self, datasingleton):
        self.datasingleton = datasingleton
        self.instruments = []

    def name(self):
        return 'Base Instruments'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Базовые инструменты'

    def initialize(self):
        self.instruments.append(PencilInstrument())
        self.instruments.append(LineInstrument())
        self.instruments.append(RectangleInstrument())

        mw = self.datasingleton.mainWindow

        base_inst_tool_bar = mw.addToolBar(self.description())
        base_inst_tool_bar.setObjectName(self.name())
        base_inst_tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        mw.base_inst_action_group = QActionGroup(base_inst_tool_bar)
        mw.base_inst_action_group.setExclusive(True)
        mw.base_inst_action_group.triggered.connect(lambda x: self.triggered_action_instrument(x))

        for inst in self.instruments:
            act = base_inst_tool_bar.addAction(inst.icon(), inst.name())
            # TODO: objectName вида <class 'baseinstruments.rectangleinstrument.RectangleInstrument'>
            # кажется неудобным, может другое значение составлять
            act.setObjectName(str(type(inst)))
            act.setToolTip(inst.description())
            act.setIcon(inst.icon())
            act.setCheckable(True)

            mw.base_inst_action_group.addAction(act)
            self.datasingleton.actionInstDict[act] = inst

    def triggered_action_instrument(self, action):
        instrument = self.datasingleton.actionInstDict[action]
        self.datasingleton.currentInstrument = instrument
