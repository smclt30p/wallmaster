from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from settings_model import SettingsModel
from settings_ui import Ui_settings_ui

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