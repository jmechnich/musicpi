#!/usr/bin/env python

import gpxpy,sys

from dateutil.tz import tzlocal

if len(sys.argv) < 2:
    print 'Usage:  gpxtest.py gpxfile'
    sys.exit(1)

gpx_file = open(sys.argv[1])

gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            print 'Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation)
            print point.time.replace(tzinfo=tzlocal()).isoformat()
