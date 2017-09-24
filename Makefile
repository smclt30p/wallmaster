install:
	mkdir -p "/usr/share/wallmaster"
	cp -R src/* /usr/share/wallmaster/.
	cp src/wallmaster /bin/wallmaster
	cp Wallmaster.desktop /usr/share/applications/.

uninstall:
	rm -rf /usr/share/wallmaster
	rm /bin/wallmaster
	rm /usr/share/applications/Wallmaster.desktop

build:
	pip3 install --user -r requirements.txt
