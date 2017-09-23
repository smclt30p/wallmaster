import subprocess
import sys
import time
import depresolv


class Main(object):

    def __init__(self):
        self.app = QApplication(sys.argv);
        self.menu = QMenu();
        self.icon = QSystemTrayIcon();
        self.timer = QTimer();
        self.engine = Engine();
        self.settings = Settings(flags=Q_FLAGS());
        self.settingsModel = SettingsModel.getSettingsModel();


    def main(self):

        # Initialize the wallpaper changer engine

        self.engine.error.connect(self.handleEngineError)
        self.timer.timeout.connect(self.engine.nextWallpaper);

        # Initialize the timer

        self.timer.start(self.settingsModel.delay * 60000);
        self.settings.delayChanged.connect(self.handleNewDelay);

        print("Changing wallpaper every {} minutes...".format(self.settingsModel.delay));

        # Initialize the menu and taskbar icon

        settingsAction = QAction("Settings");
        nextAction = QAction("Next Wallpaper");
        exitAction = QAction("Exit");
        exitAction.triggered.connect(self.saveAndExit);
        nextAction.triggered.connect(self.engine.nextWallpaper);
        settingsAction.triggered.connect(self.settings.show);
        self.menu.addAction(settingsAction);
        self.menu.addAction(nextAction);
        self.menu.addSeparator();
        self.menu.addAction(exitAction);
        self.icon.setIcon(QIcon("icon.png"));
        self.icon.setContextMenu(self.menu);
        self.icon.show();

        exit(self.app.exec_());

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

    launcher = depresolv.launch_main(["PyQt5", "bs4", "lxml", "requests"], posixdeps=["pygobject"])

    if launcher is depresolv.ALL_SATISFIED:

        flag = open("installed", "wb+")
        flag.close()

        from PyQt5.QtCore import Q_FLAGS, QTimer
        from PyQt5.QtGui import QIcon
        from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

        from engine import Engine
        from settings import Settings
        from settings_model import SettingsModel

        Main().main();

    elif launcher is depresolv.INSTALLED_AND_SATISFIED:

        subprocess.Popen([sys.executable, sys.argv])
        exit(0)

    elif launcher is depresolv.INSTALL_FAILED:
        print("Some dependencies failed to install! Please report this!")

        # Prevent CMD window from closing
        while True:
            time.sleep(1)
