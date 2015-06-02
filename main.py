#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    # from canvas import Canvas
    # c = Canvas()
    # c.show()

    sys.exit(app.exec_())