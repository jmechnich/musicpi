#!/bin/sh

DEV=/dev/rfcomm0

echo "Stopping gpsd"
killall gpsd > /dev/null 2>&1
sleep 2
killall -9 gpsd > /dev/null 2>&1

if [ -e $DEV ]; then
	sudo rfcomm release 0
fi

sleep 2

if [ -e $DEV ]; then
	echo "Could not release $DEV"
	exit 1
fi

