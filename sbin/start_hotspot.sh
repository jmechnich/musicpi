#!/bin/sh

ifdown wlan0
sleep 1
ifup wlan0=wlan0-host
