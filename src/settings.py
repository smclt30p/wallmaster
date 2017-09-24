#
# Copyright (c) 2017 Ognjen Galić
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE-
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE

from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from ui.settings_ui import Ui_settings_ui


class SettingsModel():

    def _bool(self, state):
        if type(state) is bool:
            return state;
        if state == "false": return False;
        if state == "true": return True;

    def __init__(self):
        self.settings = QSettings("wallmaster");
        self.anime = self._bool(self.settings.value("anime", True));
        self.people = self._bool(self.settings.value("people", True));
        self.general = self._bool(self.settings.value("general", True));
        self.nsfw = self._bool(self.settings.value("nsfw", True));
        self.delay = int(self.settings.value("delay", 15));
        self.interests = self.settings.value("interests", "");

    def save(self):
        self.settings.setValue("anime", self.anime);
        self.settings.setValue("people", self.people);
        self.settings.setValue("general", self.general);
        self.settings.setValue("nsfw", self.nsfw);
        self.settings.setValue("interests", self.interests);
        self.settings.setValue("delay", self.delay);

    anime = True;
    people = True;
    general = True;
    nsfw = False;
    interests = "";
    delay = 15;

    instance = None;

    @staticmethod
    def getSettingsModel():
        if SettingsModel.instance is None:
            SettingsModel.instance = SettingsModel();
        return SettingsModel.instance;

class Settings(QDialog):

    delayChanged = pyqtSignal(int);

    def __init__(self, flags, *args, **kwargs):

        super().__init__(flags, *args, **kwargs);
        self.ui = Ui_settings_ui();
        self.ui.setupUi(self);

        self.setWindowTitle("Wallmaster Settings");
        self.setWindowIcon(QIcon("icon.png"));

        self.settings = SettingsModel.getSettingsModel();

        self.ui.anime.setChecked(self.settings.anime);
        self.ui.people.setChecked(self.settings.people);
        self.ui.general.setChecked(self.settings.general);
        self.ui.nsfw.setChecked(self.settings.nsfw);
        self.ui.lineEdit.setText(self.settings.interests);
        self.ui.spinBox.setValue(self.settings.delay);
        self.ui.spinBox.valueChanged.connect(self.handeDelayChange);

        self.ui.close.clicked.connect(self.handleClose);

        self.ui.anime.stateChanged.connect(self.handleCheckboxChange);
        self.ui.people.stateChanged.connect(self.handleCheckboxChange);
        self.ui.general.stateChanged.connect(self.handleCheckboxChange);
        self.ui.nsfw.stateChanged.connect(self.handleCheckboxChange);
        self.ui.lineEdit.textChanged.connect(self.handleNewInterest)

    def closeEvent(self, event):
        event.ignore();
        self.handleClose();

    def handleClose(self):
        self.settings.save();
        self.delayChanged.emit(self.settings.delay);
        self.hide();

    def handleCheckboxChange(self, inc):
        sender = self.sender();

        state = self.stateToBool(inc);

        if sender is self.ui.anime:
            self.settings.anime = state;
        if sender is self.ui.people:
            self.settings.people = state;
        if sender is self.ui.general:
            self.settings.general = state;
        if sender is self.ui.nsfw:
            self.settings.nsfw = state;

    def stateToBool(self, state):
        if state == 0: return False;
        if state == 2: return True;

    def handeDelayChange(self, value):
        self.settings.delay = value;

    def handleNewInterest(self, interest):
        self.settings.interests = interest;