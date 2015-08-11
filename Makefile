PREFIX = /usr

all:
	deepin-generate-mo locale/locale_config.ini

install:
	mkdir -p ${DESTDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${PREFIX}/share/applications
	cp src/main.py ${DESTDIR}${PREFIX}/bin/mirror-switching-tool
	cp misc/*.desktop ${DESTDIR}${PREFIX}/share/applications/
	cp -r locale/mo ${DESTDIR}${PREFIX}/share/locale
	chmod 755 ${DESTDIR}${PREFIX}/bin/mirror-switching-tool
