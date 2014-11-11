musicpi
=======

A collection of scripts for running a Raspberry Pi based music server

## Features

- Trimmed down standard Raspbian Wheezy system (~1.5 GB)
- Music collection stored on USB disk
- Additional music can be stored on a ramdisk temporily
- File access via *samba*
- Music playback via *MPD* and *shairport* (https://github.com/abrasive/shairport)
- Automount usb device with *usbmount*
- Use *hostapd* to provide own (unencrypted) wifi network for easy access and remote control of MPD
- Use RPi GPIO to signal system state changes with an LED and monitor a shutdown switch

## Additional notes

- *shairplay* is available from Debian repo and might work just as well as shairport (not tested)
- When bringing up the wifi interface, the system will look for a known (encrypted) network first and only start its own access point if none was found. Rename/move `/etc/wpa_supplicant/wpa_supplicant.conf` to force AP startup.

## Plans and ideas

- Add wardriving/GPS logging functionality (for in-car use), maybe also use GPS for syncing clock of RPi?
- Add light-weight webserver with MPD client interface

## Random comments

This project is heavily inspired by other distros serving a similar purpose, notably volumio (http://volumio.org) which has a great UI and runs very smoothly unless you want to customize the system (broken packages, non-standard daemon management, etc)

## Related projects

- qmpc - MPD client for the Nokia N900 (https://github.com/jmechnich/qmpc)

## Dependencies

- python-dateutil
- python-gps
- python-rpi.gpio
