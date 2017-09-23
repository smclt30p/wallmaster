import platform
import subprocess

from PyQt5.QtCore import QThread, QTemporaryDir, pyqtSignal, QDir

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

            print("Writing pic to {}/wp.jpg".format(QDir.temp().path()));

            tempfile = open(QDir.temp().path() + "/wp.jpg", "wb+");
            tempfile.write(picBytes);
            tempfile.close();
            self.change_wallpaper()

            print("Wallpaper changed");

        except Exception as ex:
            print("Exception occured: " + str(ex));
            self.error.emit(str(ex));

    def nextWallpaper(self):
        self.temp = QTemporaryDir();
        if not self.temp.isValid():
            print("tmp dir not valid...");
            return;
        self.start();

    def change_wallpaper(self):

        if platform.system() == "Linux":
            if subprocess.check_call(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file:///tmp/wp.jpg"]) != 0:
                raise Exception("Wallpaper setting failed!")
            return
        if platform.system() == "Windows":
            import ctypes
            ctypes.windll.user32.SystemParametersInfoW(20, 0, QDir.temp().path() + "/wp.jpg", 0);
            pass