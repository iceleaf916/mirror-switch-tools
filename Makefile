PREFIX = /usr

all:

install:
	mkdir -p ${DESTDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${PREFIX}/share/applications
	cp src/main.py ${DESTDIR}${PREFIX}/bin/mirror-switch-tools
	cp misc/*.desktop ${DESTDIR}${PREFIX}/share/applications/
	chmod 755 ${DESTDIR}${PREFIX}/bin/mirror-switch-tools
