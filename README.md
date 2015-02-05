musicpi
=======

A collection of scripts for running a Raspberry Pi based music server

## Features

- Trimmed down standard Raspbian Wheezy system (~1.5 GB)
- Music collection stored on USB disk
- Additional music can be stored on a ramdisk temporarily
- File access via *samba*
- Music playback via *MPD*
- Audio streaming via *gmediarender-resurrect* (UPnP) and *shairport* (Airplay)
- Automount usb device with *usbmount*
- Use *hostapd* to provide own (unencrypted) wifi network for easy access and remote control of MPD
- Use RPi GPIO to signal system state changes with an LED and monitor a shutdown switch
- MPD web interface using *ympd*
- GPS location logging using *gpxlogger* (GPX) and *gpspipe* (NMEA)
- WiFi AP logging using *iwlist scan* or *wpa_cli scan(_results)*

## Additional notes

- *shairplay* is available from Debian repo and might work just as well as shairport (not tested)
- When bringing up the wifi interface, the system will look for a known (encrypted) network first and only start its own access point if none was found. Rename/move `/etc/wpa_supplicant/wpa_supplicant.conf` to force AP startup.

## Random comments

This project is heavily inspired by other distros serving a similar purpose, notably volumio (http://volumio.org) which has a great UI and runs very smoothly unless you want to customize the system (broken packages, non-standard daemon management, etc).

## Related projects

- qmpc - MPD client for the Nokia N900 (https://github.com/jmechnich/qmpc)

## Dependencies

- python-dateutil
- python-gps
- python-rpi.gpio
- cmake
- libmpdclient-dev

## Hardware

After multiple iterations the final system consists of:

- Unused WD external harddisk case
- Raspberry Pi Model B
- Adafruit 16x2 RGB LCD Pi Plate
- Adafruit PermaProto Pi
- Adafruit Ultimate GPS Breakout
- Edimax EW-7811Un Wireless Adapter
- Red status LED
- Power off switch
- WD Elements 2.5" HDD 1TB

An external USB hub was used at some point along the way but has proven itself to be just an additional source of power-related instabilities. It was removed and the 5V DC supply for the micro USB connector connected directly to the power input. As a downside, no additional USB ports are available.

#### Outside view
![](https://raw.github.com/jmechnich/musicpi/master/pics/Outside.jpg)

#### Inside view
![](https://raw.github.com/jmechnich/musicpi/master/pics/Inside.jpg)

#### Connectors
![](https://raw.github.com/jmechnich/musicpi/master/pics/Connectors.jpg)
