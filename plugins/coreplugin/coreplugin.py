__author__ = 'ipetrash'

from iplugin import IPlugin
from PySide.QtGui import *

class PluginCore(IPlugin):
    def __init__(self, application):
        # TODO: rem
        from .foo import say
        say('{} {} {}'.format(self,  'init', application))

        pass
        # self.window = QMainWindow()
        # self.window.show()

    def name(self):
        return 'Core Plugin'

    def version(self):
        return '0.0.1'

    def description(self):
        return 'Базовый плагин'

    def initialize(self):
        pass