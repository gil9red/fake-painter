__author__ = 'ipetrash'


from abc import *


class IPlugin(metaclass=ABCMeta):
    @abstractmethod
    def init(self, *args, **kwargs):
        """"""

    @abstractproperty
    def name(self):
        """Свойство должно возвращать имя плагина"""

    @abstractproperty
    def version(self):
        """Свойство должно возвращать строку, описывающую версию плагина в формате 'x.y.z'"""

    @abstractproperty
    def description(self):
        """Свойство должно возвращать описание плагина"""