# -*- coding: UTF-8 -*-

import os
import os.path
import sys

from iplugin import IPlugin

# TODO: брать из синглетона-настроек
# from outwiker.gui.guiconfig import PluginsConfig


class PluginsLoader:
    """
    Класс для загрузки плагинов
    """
    def __init__(self, application):
        self.__application = application

        # Словарь с загруженными плагинами
        # Ключ - имя плагина
        # Значение - экземпляр плагина
        self.__plugins = {}

        # Словарь с плагинами, которые были отключены пользователем
        # Ключ - имя плагина
        # Значение - экземпляр плагина
        self.__disabled_plugins = {}

        # Пути, где ищутся плагины
        self.__dirlist = []

        # Имя классов плагинов должно начинаться с "Plugins"
        self.__pluginsStartName = "Plugin"

        # Установить в False, если не нужно выводить ошибки(например, в тестах)
        self.enableOutput = True

    def _print(self, text):
        if self.enableOutput:
            print(text)

    @property
    def disabled_plugins(self):
        """
        Возвращает список отключенных плагинов
        """
        return self.__disabled_plugins

    def update_disable_list(self):
        """
        Обновление состояния плагинов. Одни отключить, другие включить
        """

        # TODO: брать из синглетона-настроек
        # options = PluginsConfig(self.__application.config)
        #
        # # Пройтись по включенным плагинам и отключить те,
        # # что попали в черный список
        # self.__disableEnabledPlugins(options.disabledPlugins.value)
        #
        # # Пройтись по отключенным плагинам и включить те,
        # # что не попали в "черный список"
        # self.__enableDisabledPlugins(options.disabledPlugins.value)

    def __disable_enabled_plugins(self, disable_list):
        """
        Отключить загруженные плагины, попавшие в "черный список"(disableList)
        """
        for pluginname in disable_list:
            if pluginname in self.__plugins.keys():
                self.__plugins[pluginname].destroy()

                assert pluginname not in self.__disabled_plugins
                self.__disabled_plugins[pluginname] = self.__plugins[pluginname]
                del self.__plugins[pluginname]

    def __enable_disabled_plugins(self, disable_list):
        """
        Включить отключенные плагины, если их больше нет в "черном списке"
        """
        for plugin in self.__disabled_plugins.values():
            if plugin.name not in disable_list:
                plugin.initialize()

                assert plugin.name not in self.__plugins
                self.__plugins[plugin.name] = plugin

                del self.__disabled_plugins[plugin.name]

    def load(self, dirlist):
        """
        Загрузить плагины из указанных директорий.
        Каждый вызов метода load() добавляет плагины в список загруженных плагинов, не очищая его
        dirlist - список директорий, где могут располагаться плагины. Каждый плагин расположен в своей поддиректории
        """
        assert dirlist is not None

        for currentDir in dirlist:
            if os.path.exists(currentDir):
                dirPackets = sorted(os.listdir(currentDir))

                # Добавить путь до currentDir в sys.path
                fullpath = os.path.abspath(currentDir)

                # TODO: странное место
                syspath = [item for item in sys.path]

                if fullpath not in syspath:
                    sys.path.insert(0, fullpath)

                # Все поддиректории попытаемся открыть как пакеты
                self.__import_modules(currentDir, dirPackets)

    def clear(self):
        """
        Уничтожить все загруженные плагины
        """
        map(lambda plugin: plugin.destroy(), self.__plugins.values())
        self.__plugins = {}

    def __import_modules(self, baseDir, dir_packages_list):
        """
        Попытаться импортировать пакеты
        baseDir - директория, где расположены пакеты
        dirPackagesList - список директорий(только имена директорий), возможно являющихся пакетами
        """
        assert dir_packages_list is not None

        print(dir_packages_list) # TODO: rem
        for packageName in dir_packages_list:
            print('packageName=', packageName) # TODO: rem
            # TODO: возможно, __pycache__ будет полезен
            if packageName == '__pycache__':
                continue

            packagePath = os.path.join(baseDir, packageName)

            # TODO: если проверять на файл, то можно импортировать одиночные модули
            # Проверить, что это директория
            if os.path.isdir(packagePath):
                # Список строк, описывающий возникшие ошибки во время импортирования
                # Выводятся только если не удалось импортировать ни одного модуля
                errors = []

                # Количество загруженных плагинов до импорта нового
                oldPluginsCount = len(self.__plugins) + len(self.__disabled_plugins)

                # Переберем все файлы внутри packagePath
                # и попытаемся их импортировать
                for fileName in sorted(os.listdir(packagePath)):
                    print('fileName=', fileName)  # TODO: rem
                    try:
                        module = self._import_single_module(packageName, fileName)
                        print('module=', module) # TODO: rem
                        if module is not None:
                            self.__load_plugin(module)
                    except BaseException as e:
                        errors.append("*** Plugin {package} loading error ***\n"
                                      "{package}/{fileName}\n"
                                      "{error}".format(package=packageName,
                                                       fileName=fileName,
                                                       error=str(e)))

                # Проверим, удалось ли загрузить плагин
                newPluginsCount = len(self.__plugins) + len(self.__disabled_plugins)

                # Вывод ошибок, если ни одного плагина из пакета не удалось
                # импортировать
                if newPluginsCount == oldPluginsCount and len(errors) != 0:
                    self._print(u"\n\n".join(errors))
                    self._print(u"**********\n")

    def _import_single_module(self, package_name, file_name):
        """
        Импортировать один модуль по имени пакета и файла с модулем
        """
        extension = ".py"
        result = None

        # Проверим, что файл может быть модулем
        if file_name.endswith(extension) and file_name != "__init__.py":
            modulename = file_name[: -len(extension)]
            # Попытаться импортировать модуль
            package = __import__(package_name + "." + modulename)
            result = getattr(package, modulename)

        return result

    def __load_plugin(self, module):
        """
        Найти классы плагинов и создать их экземпляры
        """
        assert module is not None

        # TODO: брать из синглетона-настроек
        # options = PluginsConfig(self.__application.config)
        #
        # for name in dir(module):
        #     self.__createObject(module,
        #                          name,
        #                          options.disabledPlugins.value)

        # Перебираем список объектов в модуле
        for name in dir(module):
            self.__create_object(module,
                                 name,
                                 # TODO: временно! заменить работающим аналогом
                                 [])

    def __create_object(self, module, name, disabled_plugins):
        """
        Попытаться загрузить класс, возможно, это плагин

        module - модуль, откуда загружается класс
        name - имя класса потенциального плагина
        """
        if name.startswith(self.__pluginsStartName):
            obj = getattr(module, name)
            if obj not in IPlugin.__subclasses__():
                return

            # if obj == Plugin or not issubclass(obj, Plugin):
            #     return

            # Создаем плагин, и в его конструктор передаем __application
            print('obj=', obj) # TODO: rem
            plugin = obj(self.__application)
            print('plugin=', plugin) # TODO: rem
            if not self.__isNewPlugin(plugin.name):
                return

            if plugin.name not in disabled_plugins:
                plugin.initialize()
                self.__plugins[plugin.name] = plugin
            else:
                self.__disabled_plugins[plugin.name] = plugin

    def __isNewPlugin(self, pluginname):
        """
        Проверка того, что плагин с таким именем еще не был загружен
        newplugin - плагин, который надо проверить
        """
        return(pluginname not in self.__plugins and
                pluginname not in self.__disabled_plugins)

    def __len__(self):
        return len(self.__plugins)

    def __getitem__(self, pluginname):
        return self.__plugins[pluginname]

    def __iter__(self):
        return self.__plugins.itervalues()
