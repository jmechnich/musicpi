#!/bin/sh

PATH=/usr/local/sbin:$PATH

GPSUSER=gps

GPXLOG_PID=`ps aux| awk '$1 ~ /^'${GPSUSER}'$/ && $11 ~ /gpxlogger$/ { print $2 }'`

if [ x$GPXLOG_PID != x ]; then
    echo 'gpxlogger is already running'
    exit 0
fi

echo "Checking gps availability and system time"
gpsdate.py || exit 0

#echo "Killing gpxlogger"
#sudo -u $GPSUSER killall gpxlogger >/dev/null 2>&1

echo "Starting gpxlogger"
sudo -u $GPSUSER gpxlogger -d -m 10 -f /home/$GPSUSER/gpx/`date +%Y%m%d-%H%M%S`.gpx
