#!/usr/bin/env python

from gps import *

mode = WATCH_ENABLE
session = gps(mode=mode)

for report in session:
    print report['class']
    print report
    print
