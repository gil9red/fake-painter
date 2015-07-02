# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Thu Jul  2 14:36:54 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(382, 286)
        self.verticalLayout = QtGui.QVBoxLayout(Settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(Settings)
        self.tabWidget.setObjectName("tabWidget")
        self.tabGeneral = QtGui.QWidget()
        self.tabGeneral.setObjectName("tabGeneral")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabGeneral)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(self.tabGeneral)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.sbWidth = QtGui.QSpinBox(self.groupBox)
        self.sbWidth.setMinimum(1)
        self.sbWidth.setMaximum(65536)
        self.sbWidth.setProperty("value", 640)
        self.sbWidth.setObjectName("sbWidth")
        self.gridLayout.addWidget(self.sbWidth, 0, 1, 1, 1)
        self.cbKindSize = QtGui.QComboBox(self.groupBox)
        self.cbKindSize.setObjectName("cbKindSize")
        self.cbKindSize.addItem("")
        self.gridLayout.addWidget(self.cbKindSize, 1, 2, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.sbHeight = QtGui.QSpinBox(self.groupBox)
        self.sbHeight.setMinimum(1)
        self.sbHeight.setMaximum(65536)
        self.sbHeight.setProperty("value", 480)
        self.sbHeight.setObjectName("sbHeight")
        self.gridLayout.addWidget(self.sbHeight, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.sbHistoryDepth = QtGui.QSpinBox(self.groupBox)
        self.sbHistoryDepth.setMaximum(1024)
        self.sbHistoryDepth.setProperty("value", 40)
        self.sbHistoryDepth.setObjectName("sbHistoryDepth")
        self.gridLayout.addWidget(self.sbHistoryDepth, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tabGeneral, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Settings)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QtGui.QApplication.translate("Settings", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Settings", "Image", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Settings", "Height:", None, QtGui.QApplication.UnicodeUTF8))
        self.cbKindSize.setItemText(0, QtGui.QApplication.translate("Settings", "px", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Settings", "Width:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Settings", "History depth:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGeneral), QtGui.QApplication.translate("Settings", "General", None, QtGui.QApplication.UnicodeUTF8))

