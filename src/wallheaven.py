from random import randint

import requests
from bs4 import BeautifulSoup


class Wallhaven:

    SEARCH_ENDPOINT = "https://alpha.wallhaven.cc/search?q={}&search_image=&categories={}&purity={}&sorting=random&order=desc&ratios=4x3,5x4,16x9,16x10";

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

        print("Searching wallpapers");

        url = self.SEARCH_ENDPOINT.format(search, categories, purity);
        response = requests.get(url, timeout=20);
        if response.status_code != 200:
            raise Exception("No internet connection or fetch failed.");

        html = BeautifulSoup(response.text, "lxml");
        data = html.find_all(attrs={"class": "preview"});
        if (len(data)) == 0:
            raise Exception("No pictures found matching your interest \"{}\".".format(search));

        print("Downloading image");

        url = data[randint(0, len(data) - 1)].attrs["href"].split("/")[-1];
        response = requests.get("https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-{}.jpg".format(url), timeout=90);
        if response.status_code != 200:
            raise Exception("Wallpaper download failed with code {}".format(response.status_code));

        return response.content;

