# ---------------------------------------------------------------------------- #
## \file Makefile
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
PYVER = $(shell python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
PYDIR = .local/lib/python$(PYVER)/site-packages
PYBLUEZ = $(HOME)/$(PYDIR)/bluetooth
PYDBUS = $(HOME)/$(PYDIR)/pydbus
BSERV = /lib/systemd/system/bluetooth.service
N ?= 1
NDEV = $$(($(N) + 1))

.SUFFIXES:

.PHONY: all
all: $(PYBLUEZ) $(PYDBUS)
	@./main.py

$(PYBLUEZ):
	@pip3 install git+https://github.com/pybluez/pybluez.git#egg=pybluez

$(PYDBUS):
	@pip3 install pydbus

.PHONY: desktop
desktop: $(HOME)/.local/share/applications/kitris.desktop icon
$(HOME)/.local/share/applications/kitris.desktop: install.sh
	@./$< $@

.PHONY: icon
icon: data data/icon.png
data:
	@mkdir $@
data/icon.png: data/kitris.svg
	@convert -resize 512x512 $< $@
data/kitris.svg: icon.py
	@./$< $@

.PHONY: build
build: icon
	@buildozer android debug

.PHONY: release-apk
release-apk: icon
	@buildozer --profile release android debug

.PHONY: release
release:
	@./release.sh "kitris"

.PHONY: install
install:
	@adb install -r bin/*.apk

.PHONY: piscan
piscan:
	@test $(USER) = root || (echo "Usage: sudo make piscan" && false)
	@test -d /home/$(SUDO_USER)/$(PYDIR)/bluetooth || (echo "todo: pip3 install pybluez" && false)
	@grep -q '/bluetoothd -C' $(BSERV) || (sed -i 's@/bluetoothd@/bluetoothd -C@' $(BSERV) && systemctl daemon-reload && systemctl restart bluetooth)
	@/usr/sbin/rfkill unblock bluetooth
	@sleep 1
	@hciconfig hci0 piscan
	@chmod o+rw /var/run/sdp

.PHONY: list
list:
	@bt-device -l | sed 1d | cat -n

.PHONY: send
send:
	@ADDR=`bt-device -l | tee /dev/stderr | sed -n $(NDEV)p | cut -d '(' -f 2 | cut -d ')' -f 1` &&\
	 echo "ADDR=$$ADDR" &&\
	 test -n "$$ADDR" &&\
	 bt-obex -p $$ADDR bin/*.apk

.PHONY: debug
debug:
	@adb shell logcat | grep python

.PHONY: tar
tar:
	@cd .. && tar cvzf kitris.tgz\
	 kitris/*.py\
	 kitris/*.md\
	 kitris/*.txt\
	 kitris/Makefile
