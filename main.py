#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'

from PySide.QtGui import *
from PySide.QtCore import *
import sys


# TODO: сделать скрипт, который проверял бы код
# pip install pyflakes pep8 pylint
# pyflakes *.py
# pep8 *.py
# pylint *.py


# TODO: генерация формы / файла ресурсов
# pyside-uic -o widget.py widget.ui
# pyside-rcc -o resource_rc.py resource.qrc

# TODO: избавиться от import * -- много лишнего импортируется

# from mainwindow import mainWindow

# TODO: может при закрытии последней вкладки, закрывать программу?
# TODO: при закрытии окна, закрывать вкладки, проверять на изменения
# TODO: обозвать как-нибудь дефолтный toolbar

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print('MAIN')
    # import datasingleton
    # print('datasingleton=', dir(datasingleton))
    from datasingleton import DataSingleton

    # print('datasingleton=', dir(datasingleton))

    # # mainWindow = MainWindow()
    # mainWindow = DataSingleton.mainWindow
    # mainWindow.show()

    DataSingleton.mainWindow.show()

    sys.exit(app.exec_())
