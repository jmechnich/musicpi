#!/bin/sh

PATH=/usr/local/sbin:/usr/local/bin:$PATH

PROGRAM=scan_wlan
GPSUSER=gps

OPTIONS="-d -n 5 -o"
OUTPATH=/home/$GPSUSER/wifi
OUTFILE=`date +%Y%m%d-%H%M%S`.json

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
