# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pluginmanager.ui'
#
# Created: Mon Jul  6 16:49:38 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PluginManager(object):
    def setupUi(self, PluginManager):
        PluginManager.setObjectName("PluginManager")
        PluginManager.resize(382, 286)
        self.verticalLayout = QtGui.QVBoxLayout(PluginManager)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(PluginManager)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.view = QtGui.QListView(self.splitter)
        self.view.setObjectName("view")
        self.description = QtGui.QTextEdit(self.splitter)
        self.description.setObjectName("description")
        self.verticalLayout.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(PluginManager)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PluginManager)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), PluginManager.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), PluginManager.reject)
        QtCore.QMetaObject.connectSlotsByName(PluginManager)

    def retranslateUi(self, PluginManager):
        PluginManager.setWindowTitle(QtGui.QApplication.translate("PluginManager", "Plugin Manager", None, QtGui.QApplication.UnicodeUTF8))

