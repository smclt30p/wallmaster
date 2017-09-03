from ctypes import *

import sys

from PyQt5.QtCore import Q_FLAGS, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

from engine import Engine
from settings import Settings
from settings_model import SettingsModel


class Main():

    def main(self):

        self.app = QApplication(sys.argv);
        self.engine = Engine();
        self.engine.error.connect(self.handleEngineError)

        self.settingsModel = SettingsModel.getSettingsModel();
        self.settings = Settings(flags=Q_FLAGS());

        self.timer = QTimer();
        self.timer.start(self.settingsModel.delay * 60000);
        self.timer.timeout.connect(self.nextActionHandler);

        self.settings.delayChanged.connect(self.handleNewDelay);

        print("Changing wallpaper every {} minutes...".format(self.settingsModel.delay));

        settingsAction = QAction("Settings");
        nextAction = QAction("Next Wallpaper");
        exitAction = QAction("Exit");

        exitAction.triggered.connect(self.saveAndExit);
        nextAction.triggered.connect(self.nextActionHandler);
        settingsAction.triggered.connect(self.settingsActionHandler);

        menu = QMenu();
        menu.addAction(settingsAction);
        menu.addAction(nextAction);
        menu.addSeparator();
        menu.addAction(exitAction);

        self.icon = QSystemTrayIcon();
        self.icon.setIcon(QIcon("icon.png"));
        self.icon.setContextMenu(menu);
        self.icon.show();

        exit(self.app.exec_());

    def settingsActionHandler(self):
        self.settings.show();

    def nextActionHandler(self):
        print("Next...");
        self.engine.nextWallpaper();

    def handleEngineError(self, error):
        self.icon.showMessage("Wallmaster", error);

    def saveAndExit(self):
        self.settings = SettingsModel.getSettingsModel();
        self.settings.save();
        self.app.exit(0);

    def handleNewDelay(self, delay):
        self.timer.stop();
        self.timer.start(delay * 60000);
        print("Setting delay to {} minutes".format(delay));

if __name__ == "__main__":
    Main().main();
