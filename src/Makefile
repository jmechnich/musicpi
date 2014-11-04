SBIN_PROGRAMS = usbreset
PY_PACKAGES   = Adafruit_Python_CharLCD musicpi_lcd
PACKAGES      = shairport gmrender-resurrect

all: default

Adafruit_Python_CharLCD:
	git clone git@github.com:adafruit/Adafruit_Python_CharLCD.git

musicpi_lcd:
	git clone git@github.com:jmechnich/musicpi_lcd.git

shairport:
	git clone git@github.com:abrasive/shairport.git

gmrender-resurrect:
	git clone git@github.com:hzeller/gmrender-resurrect.git

PACKAGES_STAMPS = $(PACKAGES:%=.%.stamp)

default: $(SBIN_PROGRAMS:%=../sbin/%) $(PACKAGES_STAMPS)

%.stamp:
	cd `echo $@ | sed 's,^\.\([^\.]\+\)\.stamp,\1,'` && make
	touch $@

usbreset: usbreset.c

../sbin/usbreset: usbreset
	cp $^ $@

install: $(PY_PACKAGES) $(PACKAGES_STAMPS)
	for p in $(PY_PACKAGES); do \
	  (cd $$p && python setup.py install); \
	done
	for p in $(PACKAGES); do\
	  (cd $$p && make install); \
	done

clean:
	rm -f $(SBIN_PROGRAMS) *~
