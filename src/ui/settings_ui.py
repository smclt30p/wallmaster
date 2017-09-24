# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_settings_ui(object):
    def setupUi(self, settings_ui):
        settings_ui.setObjectName("settings_ui")
        settings_ui.resize(278, 305)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(settings_ui)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.interests = QtWidgets.QGroupBox(settings_ui)
        self.interests.setObjectName("interests")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.interests)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.interests)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout_4.addWidget(self.interests)
        self.categories = QtWidgets.QGroupBox(settings_ui)
        self.categories.setObjectName("categories")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.categories)
        self.verticalLayout.setObjectName("verticalLayout")
        self.general = QtWidgets.QCheckBox(self.categories)
        self.general.setObjectName("general")
        self.verticalLayout.addWidget(self.general)
        self.anime = QtWidgets.QCheckBox(self.categories)
        self.anime.setObjectName("anime")
        self.verticalLayout.addWidget(self.anime)
        self.people = QtWidgets.QCheckBox(self.categories)
        self.people.setObjectName("people")
        self.verticalLayout.addWidget(self.people)
        self.verticalLayout_4.addWidget(self.categories)
        self.settings = QtWidgets.QGroupBox(settings_ui)
        self.settings.setObjectName("settings")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.settings)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.nsfw = QtWidgets.QCheckBox(self.settings)
        self.nsfw.setStyleSheet("QCheckBox {\n"
"    color: red;\n"
"}")
        self.nsfw.setObjectName("nsfw")
        self.verticalLayout_3.addWidget(self.nsfw)
        self.label = QtWidgets.QLabel(self.settings)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.settings)
        self.spinBox.setMinimum(5)
        self.spinBox.setMaximum(1000)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_3.addWidget(self.spinBox)
        self.verticalLayout_4.addWidget(self.settings)
        self.buttons = QtWidgets.QHBoxLayout()
        self.buttons.setObjectName("buttons")
        spacerItem = QtWidgets.QSpacerItem(16, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons.addItem(spacerItem)
        self.close = QtWidgets.QPushButton(settings_ui)
        self.close.setObjectName("close")
        self.buttons.addWidget(self.close)
        self.verticalLayout_4.addLayout(self.buttons)
        self.close.raise_()
        self.categories.raise_()
        self.interests.raise_()
        self.anime.raise_()
        self.settings.raise_()

        self.retranslateUi(settings_ui)
        QtCore.QMetaObject.connectSlotsByName(settings_ui)

    def retranslateUi(self, settings_ui):
        _translate = QtCore.QCoreApplication.translate
        settings_ui.setWindowTitle(_translate("settings_ui", "Dialog"))
        self.interests.setTitle(_translate("settings_ui", "Interests"))
        self.categories.setTitle(_translate("settings_ui", "Categories"))
        self.general.setText(_translate("settings_ui", "General"))
        self.anime.setText(_translate("settings_ui", "Anime"))
        self.people.setText(_translate("settings_ui", "People"))
        self.settings.setTitle(_translate("settings_ui", "Settings"))
        self.nsfw.setText(_translate("settings_ui", "NSFW"))
        self.label.setText(_translate("settings_ui", "Delay (minutes)"))
        self.close.setText(_translate("settings_ui", "Close"))

