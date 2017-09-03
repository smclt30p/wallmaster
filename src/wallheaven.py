from random import randint

import requests
from bs4 import BeautifulSoup


class Wallhaven:

    SEARCH_ENDPOINT = "https://alpha.wallhaven.cc/search?q={}&search_image=&categories={}&purity={}&sorting=random&order=desc&ratios=16x9";

    def random(self, search="", people=True, general=True, anime=True, nsfw=False):
        categories = ["0", "0", "0"];
        purity = "101";
        if general:
            categories[0] = "1";
        if anime:
            categories[1] = "1";
        if people:
            categories[2] = "1";
        if nsfw:
            purity = "010";
        categories = "".join(categories);

        print("Fetching search...");

        url = self.SEARCH_ENDPOINT.format(search, categories, purity);
        response = requests.get(url, timeout=20);
        if response.status_code != 200:
            raise Exception("No internet connection or fetch failed.");

        html = BeautifulSoup(response.text, "lxml");
        data = html.find_all(attrs={"class": "preview"});
        if (len(data)) == 0:
            raise Exception("No pictures found matching your interest \"{}\".".format(search));

        print("Fetching metadata...");

        url = data[randint(0, len(data) - 1)].attrs["href"];
        response = requests.get(url, timeout=20);
        if response.status_code != 200:
            raise Exception("Failed to download the new picture.");

        print("Downloading wallpaper...");

        html = BeautifulSoup(response.text, "lxml");
        data = html.find_all(attrs={"id":"wallpaper"});
        if (len(data)) == 0:
            raise Exception("Image fetch failed: broken code");

        print("Fetching wallpaper...");

        url = "http:" + data[0].attrs["src"];
        response = requests.get(url, timeout=90);
        if response.status_code != 200:
            raise Exception("Wallpaper download failed...");

        return response.content;

