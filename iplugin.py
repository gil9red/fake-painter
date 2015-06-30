#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'


from abc import *


class IPlugin(metaclass=ABCMeta):
    @abstractproperty
    def name(self):
        """Свойство должно возвращать имя плагина"""

    @abstractproperty
    def version(self):
        """Свойство должно возвращать строку, описывающую версию плагина в формате 'x.y.z'"""

    @abstractproperty
    def description(self):
        """Свойство должно возвращать описание плагина"""

    @abstractmethod
    def initialize(self, *args, **kwargs):
        """"""

    # def __str__(self):
    #     return '{} ({})'.format(self.name(), self.version())