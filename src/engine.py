import ctypes

from PyQt5.QtCore import QThread, QTemporaryDir, pyqtSignal

from settings_model import SettingsModel
from wallheaven import Wallhaven


class Engine(QThread):

    error = pyqtSignal(str);

    def __init__(self):
        super().__init__();
        self.wallhaven = Wallhaven();
        self.settings = SettingsModel.getSettingsModel();

    def run(self):

        try:

            picBytes = self.wallhaven.random(search=self.settings.interests,
                                  people=self.settings.people,
                                  anime=self.settings.anime,
                                  general=self.settings.general,
                                  nsfw=self.settings.nsfw);

            if (picBytes) == None:
                print("Pic fetch failed...");
                return;

            print("Writing pic to file...");

            tempfile = open(self.temp.path() + "/wp.jpg", "wb+");
            tempfile.write(picBytes);
            tempfile.close();

            ctypes.windll.user32.SystemParametersInfoW(20, 0, self.temp.path() + "/wp.jpg", 0);

        except Exception as ex:
            print("Exception occured: " + str(ex));
            self.error.emit(str(ex));

    def nextWallpaper(self):
        self.temp = QTemporaryDir();
        if not self.temp.isValid():
            print("tmp dir not valid...");
            return;
        self.start();