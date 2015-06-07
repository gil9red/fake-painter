__author__ = 'ipetrash'

from iplugin import IPlugin
from PySide.QtGui import *

class CorePlugin(IPlugin):
    def init(self, *args, **kwargs):
        pass
        # self.window = QMainWindow()
        # self.window.show()

    def name(self):
        return 'Core Plugin'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Базовый плагин'