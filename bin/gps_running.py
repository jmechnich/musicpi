#!/usr/bin/env python

import os, sys
from serial import Serial

devlist = []
if os.path.exists( '/etc/default/gpsd'):
    f = open('/etc/default/gpsd')
    for line in f:
        if line.strip().startswith('DEVICES'):
            devs = ''.join(line.split('=')[1:])
            if devs.startswith('"') or devs.startswith("'"):
                devs = eval(devs)
            devlist = devs.split()

for dev in devlist:
    try:
        print "Trying", dev
        conn = Serial(port=dev,baudrate=9600,timeout=5)
        conn.open()
        conn.close()
        print "GPS is online (%s)" % dev
        break
    except:
        continue
else:
    print "GPS is offline"
    sys.exit(1)

sys.exit(0)
