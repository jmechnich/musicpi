#!/bin/sh

PATH=/usr/local/sbin:$PATH

PROGRAM=gpxlogger
GPSUSER=gps

OPTIONS="-d -m 10 -f"
OUTPATH=/home/$GPSUSER/gpx
OUTFILE=`date +%Y%m%d-%H%M%S`.gpx

PROGRAM_PID=`ps aux| awk '$1 ~ /^'${GPSUSER}'$/ && $11 ~ /'$PROGRAM'$/ { print $2 }'`
if [ x$PROGRAM_PID != x ]; then
    echo "$PROGRAM is already running"
    exit 0
fi

echo "Checking gps availability and system time"
gpsdate.py || exit 0

#echo "Killing $PROGRAM"
#sudo -u $GPSUSER killall $PROGRAM >/dev/null 2>&1

echo "Starting $PROGRAM"
[ ! -d $OUTPATH ] && (sudo -u $GPSUSER mkdir -p $OUTPATH; echo "Creating $OUTPATH")
sudo -u $GPSUSER $PROGRAM $OPTIONS $OUTPATH/$OUTFILE
