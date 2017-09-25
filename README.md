![Screenshot](https://i.imgur.com/b9p04uV.png)
# Dynamic Wallpaper Changer
### for Windows and GNOME 3

This is a dynamic wallpaper changer that pulls wallpapers from
Wallhaven based on your query and categories and applies it.

This is based on a scraper, not an API. Sorry Wallhaven.
[They don't take money](https://alpha.wallhaven.cc/forums/thread/326?page=1), so if you
are good with PHP/Laravel, go make something awesome there. Hardware and
bandwidth is also welcome.

A few 404 errors are expected, that's not a issue I can resolve.
I mean, I could, but I would need to increase the traffic towards
Wallhaven by 33%, and I don't want to do that.

Windows installers coming soon, as well as Linux packages.

__Thanks to mervick for the awesome Dracula theme! Get it [here](https://github.com/mervick/Qt-Creator-Darcula)__

*The Dracula theme is licensed under the GNU GPL*

__*This project is released under the BSD 2-clause license. See LICENSE.md*__

### How to install (for now)

## Windows

1) Download Python 3 from python.org, and check "Add to PATH" during install.
2) Run `pip install -r requirements.win.txt`
3) Make a shortcut to start.bat and put it inside the Startup folder
4) Run it!

## GNOME 3

1) Install Python 3 from your distributions repos
2) Install the dependencies with pip (`make build`) OR use the packages provided by your distribution
3) Run `make install`
4) Search for `wallmaster` in your applications and run it!