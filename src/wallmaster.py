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

import subprocess
import sys
import platform
import requests

from PyQt5.QtCore import Q_FLAGS, QTimer, pyqtSignal, QDir, QTemporaryDir, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

from settings import SettingsModel, Settings
from bs4 import BeautifulSoup
from random import randint


class Engine(QThread):

    error = pyqtSignal(str)
    WALLHAVEN_SEARCH = "https://alpha.wallhaven.cc/search?q={}&search_image=&categories={}&purity={}&sorting=random&order=desc&ratios=4x3,5x4,16x9,16x10"

    def __init__(self):
        super().__init__()
        self.settings = SettingsModel.getSettingsModel()

    def run(self):
        try:
            picBytes = self.wallhaven_random(search=self.settings.interests,
                                             people=self.settings.people,
                                             anime=self.settings.anime,
                                             general=self.settings.general,
                                             nsfw=self.settings.nsfw)

            if picBytes is None:
                print("Pic fetch failed...")
                return

            print("Writing pic to {}/wp.jpg".format(QDir.temp().path()))
            tempfile = open(QDir.temp().path() + "/wp.jpg", "wb+")
            tempfile.write(picBytes)
            tempfile.close()
            self.change_wallpaper()
            print("Wallpaper changed")

        except Exception as ex:
            print("Exception occured: " + str(ex))
            self.error.emit(str(ex))

    def next_wallpaper(self):
        self.temp = QTemporaryDir()

        if not self.temp.isValid():
            print("tmp dir not valid...")
            return

        self.start()

    def change_wallpaper(self):

        if platform.system() == "Linux":
            if subprocess.check_call(["gsettings",
                                      "set",
                                      "org.gnome.desktop.background",
                                      "picture-uri",
                                      "file:///tmp/wp.jpg"]) != 0:
                raise Exception("Wallpaper setting failed!")
            return

        if platform.system() == "Windows":
            import ctypes
            ctypes.windll.user32.SystemParametersInfoW(20, 0, QDir.temp().path() + "/wp.jpg", 0)

    def wallhaven_random(self, search="", people=True, general=True, anime=True, nsfw=False):

        categories = ["0", "0", "0"]
        purity = "101"

        if general:
            categories[0] = "1"
        if anime:
            categories[1] = "1"
        if people:
            categories[2] = "1"
        if nsfw:
            purity = "010"

        categories = "".join(categories)
        print("Searching wallpapers")
        url = self.WALLHAVEN_SEARCH.format(search, categories, purity)
        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            raise Exception("No internet connection or fetch failed.")

        html = BeautifulSoup(response.text, "lxml")
        data = html.find_all(attrs={"class": "preview"})

        if (len(data)) == 0:
            raise Exception("No pictures found matching your interest \"{}\".".format(search))

        print("Downloading image")
        url = data[randint(0, len(data) - 1)].attrs["href"].split("/")[-1]
        response = requests.get("https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-{}.jpg".format(url),
                                timeout=90)

        if response.status_code != 200:
            raise Exception("Wallpaper download failed with code {}".format(response.status_code))

        return response.content


class Wallmaster(object):

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.menu = QMenu()
        self.icon = QSystemTrayIcon()
        self.timer = QTimer()
        self.engine = Engine()
        self.settings = Settings(flags=Q_FLAGS())
        self.settingsModel = SettingsModel.getSettingsModel()
        self.gi_initialized = False

    def main(self):

        # Initialize the stylesheet

        stylesheet = open("style/stylesheet.css", "r")
        stylesheet_str = stylesheet.read()
        stylesheet.close()
        self.app.setStyleSheet(stylesheet_str)

        # Initialize the wallpaper changer engine

        self.engine.error.connect(self.handle_engine_error)
        self.timer.timeout.connect(self.engine.next_wallpaper)

        # Initialize the timer

        self.timer.start(self.settingsModel.delay * 60000)
        self.settings.delayChanged.connect(self.change_delay)

        print("Changing wallpaper every {} minutes...".format(self.settingsModel.delay))

        # Initialize the menu and taskbar icon

        settingsAction = QAction("Settings")
        nextAction = QAction("Next Wallpaper")
        exitAction = QAction("Exit")
        exitAction.triggered.connect(self.save_and_exit)
        nextAction.triggered.connect(self.engine.next_wallpaper)
        settingsAction.triggered.connect(self.settings.show)
        self.menu.addAction(settingsAction)
        self.menu.addAction(nextAction)
        self.menu.addSeparator()
        self.menu.addAction(exitAction)
        self.icon.setIcon(QIcon("images/icon.png"))
        self.icon.setContextMenu(self.menu)
        self.icon.show()

        exit(self.app.exec_())

    def handle_engine_error(self, error):

        # try to use gnome native notifications

        try:
            import gi
            gi.require_version("Notify", "0.7")
            from gi.repository import Notify
            if not self.gi_initialized:
                Notify.init("Wallmaster")
                self.gi_initialized = True
            Notify.Notification.new(error).show()
            return
        except ImportError:
            pass

        # fall back to Qt's native baloon

        self.icon.showMessage("Wallmaster", error)

    def save_and_exit(self):

        self.settings = SettingsModel.getSettingsModel()
        self.settings.save()

        if self.gi_initialized:
            import gi
            gi.require_version("Notify", "0.7")
            from gi.repository import Notify
            Notify.uninit()

        self.app.exit(0)

    def change_delay(self, delay):
        self.timer.stop()
        self.timer.start(delay * 60000)
        print("Setting delay to {} minutes".format(delay))
