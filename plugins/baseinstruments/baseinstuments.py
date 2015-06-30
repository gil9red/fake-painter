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
# import datasingleton


class PluginBaseInstruments(IPlugin):
    def __init__(self, datasingleton):
        # TODO: обрабатывать
        print('!!! {} {} {}'.format(self,  'init', datasingleton))
        self.datasingleton = datasingleton
        self.instruments = []

    def name(self):
        return 'Base Instruments'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Базовые инструменты'

    def initialize(self):
        self.instruments.append(LineInstrument())
        self.instruments.append(PencilInstrument())
        self.instruments.append(RectangleInstrument())

        mw = self.datasingleton.mainWindow
        print('!!! init', self.datasingleton)
        base_inst_tool_bar = mw.addToolBar(self.description())
        base_inst_tool_bar.setObjectName(self.name())
        base_inst_tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # TODO: возможно, лучше создать это в MainWindow
        mw.base_inst_action_group = QActionGroup(base_inst_tool_bar)
        mw.base_inst_action_group.setExclusive(True)
        # mw.base_inst_action_group.triggered.connect(mw.triggered_action_instrument)

        # mw.base_inst_action_group.triggered.connect(lambda x: print('lambda:', x))
        # Вариант ниже почему-то не работает
        mw.base_inst_action_group.triggered.connect(lambda x: self.triggered_action_instrument(x))
        # mw.base_inst_action_group.triggered.connect(self.foo)

        for inst in self.instruments:
            act = base_inst_tool_bar.addAction(inst.icon(), inst.name())
            act.setObjectName(str(type(inst)))
            act.setToolTip(inst.description())
            act.setIcon(inst.icon())
            act.setCheckable(True)

            # print('  ***', act.triggered.connect(self.foo))

            mw.base_inst_action_group.addAction(act)
            self.datasingleton.actionInstDict[act] = inst

            # print('    ', inst, act, act.objectName())

    def triggered_action_instrument(self, action):
        # QMessageBox.information(None, '', '')
        instrument = self.datasingleton.actionInstDict[action]
        self.datasingleton.currentInstrument = instrument
        # print(self.datasingleton.currentInstrument)
    #
    # def foo(self, a):
    #     print('foo', a)
