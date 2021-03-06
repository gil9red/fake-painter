#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of fake-painter, by Ilya Petrash
# and is licensed under the MIT license, under the terms listed within
# LICENSE which is included with the source of this package

__author__ = 'ipetrash'

from PySide.QtGui import QApplication
import sys


# TODO: set/get методы заменить на свойства
# TODO: логирование https://docs.python.org/3.4/library/logging.html

# TODO: сделать скрипт, который проверял бы код
# pip install pyflakes pep8 pylint
# pyflakes *.py
# pep8 *.py
# pylint *.py


# TODO: избавиться от import * -- много лишнего импортируется

# TODO: плагин, добавляющий контекстное меню на вкладки, в котором есть
# действие открытия папки с файлом


if __name__ == '__main__':
    app = QApplication(sys.argv)

    import datasingleton

    mw = datasingleton.instance.mainWindow
    mw.show()

    sys.exit(app.exec_())
