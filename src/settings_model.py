from PyQt5.QtCore import QSettings


class SettingsModel():

    def _bool(self, state):
        if state == "false": return False;
        if state == "true": return True;

    def __init__(self):
        self.settings = QSettings("wallmaster");
        self.anime = self._bool(self.settings.value("anime", True));
        self.people = self._bool(self.settings.value("people", True));
        self.general = self._bool(self.settings.value("general", True));
        self.nsfw = self._bool(self.settings.value("nsfw", True));
        self.delay = self.settings.value("delay", 0);
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