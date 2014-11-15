SBIN_PROGRAMS = usbreset
PYPACKAGES    = Adafruit_Python_CharLCD musicpi_lcd gpxpy
PACKAGES      = shairport gmrender-resurrect ympd

all: default

usbreset: usbreset.c

Adafruit_Python_CharLCD:
	git clone git@github.com:adafruit/Adafruit_Python_CharLCD.git

musicpi_lcd:
	git clone git@github.com:jmechnich/musicpi_lcd.git

shairport:
	git clone git@github.com:abrasive/shairport.git

gmrender-resurrect:
	git clone git@github.com:hzeller/gmrender-resurrect.git

gpxpy:
	git clone git@github.com:tkrajina/gpxpy.git

ympd:
	git clone git@github.com:jmechnich/ympd.git

SBINDIR         = ../sbin
INST_PROGRAMS   = $(SBIN_PROGRAMS:%=$(SBINDIR)/%)
PACKAGES_STAMPS = $(PACKAGES:%=.%.stamp)

default: $(INST_PROGRAMS) $(PACKAGES_STAMPS)

.%.stamp: %
	cd $< && make
	touch $@

$(SBINDIR)/%: %
	cp $^ $@

install: $(PYPACKAGES) $(PACKAGES_STAMPS)
	for p in $(PYPACKAGES); do \
	  (cd $$p && python setup.py install); \
	done
	for p in $(PACKAGES); do\
	  (cd $$p && make install); \
	done

clean:
	rm -f $(SBIN_PROGRAMS)
	rm -f $(PACKAGES_STAMPS)
	for p in $(PACKAGES); do\
	  (cd $$p && make clean); \
	done
	find . -name '*~' | xargs rm -f
