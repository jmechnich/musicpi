SBIN_PROGRAMS = usbreset
PACKAGES      = musicpi_lcd

all: $(addprefix ../sbin/,$(SBIN_PROGRAMS))

usbreset: usbreset.c

../sbin/usbreset: usbreset
	cp $^ $@

$(PACKAGES):
	git clone git@github.com:jmechnich/$@.git

install: $(PACKAGES)
	for p in $(PACKAGES); do \
	  (cd $$p && python setup.py install); \
	done

clean:
	rm -f $(SBIN_PROGRAMS) *~
