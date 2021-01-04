SERVICE := marsu
DESTDIR ?= dist_root
SERVICEDIR ?= /srv/$(SERVICE)

.PHONY: build install

build:
	$(MAKE) -C src/pad

install: build
	mkdir -p $(DESTDIR)$(SERVICEDIR)
	mkdir -p $(DESTDIR)$(SERVICEDIR)/pad
	install -o root -g root -m 555 src/pad/pad $(DESTDIR)$(SERVICEDIR)/pad
	install -o root -g root -m 444 src/pad/index.html $(DESTDIR)$(SERVICEDIR)/pad

	mkdir -p $(DESTDIR)$(SERVICEDIR).static
	mkdir -p $(DESTDIR)$(SERVICEDIR)/frontend/
	cp -a src/frontend/project     $(DESTDIR)$(SERVICEDIR)/frontend/
	cp -a src/frontend/research    $(DESTDIR)$(SERVICEDIR)/frontend/
	cp -a src/frontend/researcher  $(DESTDIR)$(SERVICEDIR)/frontend/
	cp -a src/frontend/readinglist $(DESTDIR)$(SERVICEDIR)/frontend/
	install -o root -g root -m 555 src/frontend/manage.py $(DESTDIR)$(SERVICEDIR)/frontend/

	mkdir -p $(DESTDIR)$(SERVICEDIR)/lib
	cp -a src/lib/scrape/src/ArticleMetadata $(DESTDIR)$(SERVICEDIR)/lib

	mkdir -p $(DESTDIR)/etc/systemd/system
	mkdir -p $(DESTDIR)/etc/uwsgi/apps-enabled
	mkdir -p $(DESTDIR)/etc/nginx/sites-enabled
	install -m 444 systemsetup/marsu-database-setup.service $(DESTDIR)/etc/systemd/system/
	install -m 444 systemsetup/marsu-pad.service            $(DESTDIR)/etc/systemd/system/
	install -m 444 systemsetup/marsu.ini                    $(DESTDIR)/etc/uwsgi/apps-enabled/
	install -m 444 systemsetup/marsu.conf                   $(DESTDIR)/etc/nginx/sites-enabled/
	install -m 444 systemsetup/marsupad.conf                $(DESTDIR)/etc/nginx/sites-enabled/
