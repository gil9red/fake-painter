#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'

from PySide.QtGui import *
from PySide.QtCore import *
import sys

# class Singleton(object):
#     def __new__(cls):
#         if not hasattr(cls, 'instance'):
#              cls.instance = super(Singleton, cls).__new__(cls)
#         return cls.instance
#
# a = Singleton()
# b = Singleton()
# print(a is b)

# TODO: сделать скрипт, который проверял бы код
# pip install pyflakes pep8 pylint
# pyflakes *.py
# pep8 *.py
# pylint *.py


# TODO: генерация формы / файла ресурсов
# pyside-uic -o widget.py widget.ui
# pyside-rcc -o resource_rc.py resource.qrc

from mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())