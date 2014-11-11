#!/bin/sh

DEV=/dev/rfcomm0

if [ ! -e $DEV ]; then
	sudo rfcomm bind 0
fi

sleep 2

if [ ! -e $DEV ]; then
	echo "Could not bind $DEV"
	exit 1
fi

echo "Starting gpsd"
killall gpsd > /dev/null 2>&1
gpsd -G $DEV
