#!/bin/sh

GWY=`/sbin/route -n | grep '^0.0.0.0' | awk '{ print $2 }'`

if [ x"$GWY" != x ]; then
	ping -q -c2 -t10 $GWY
fi
