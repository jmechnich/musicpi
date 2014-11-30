#!/usr/bin/python

import os, subprocess, sys, time

debug = False
#debug = True

def scan_essids():
    lines = [ line.strip().replace('"','').split(':')[1] for line in subprocess.check_output(
        ["/sbin/iwlist","wlan0","scan"]).split("\n")
              if line.strip().startswith("ESSID") ]
    
    lines = list(set(lines))
    return [ l for l in lines if len(l) ]

def scan_wpasupplicant():
    wspath = "/etc/wpa_supplicant/wpa_supplicant.conf"
    if not os.path.exists(wspath): return []
    lines = [ line.strip().replace('"','').split('=')[1] for line in open(wspath)
              if line.strip().startswith("ssid") ]
    
    return [ l for l in lines if len(l) ]
	

subprocess.call(["/sbin/ifconfig","wlan0","up"])
subprocess.call(["/sbin/ifconfig","wlan0","down"])

retries = 3
essids_found = []
while retries > 0:
    essids_found = scan_essids()
    if len(essids_found): break
    retries -= 1
    time.sleep(1)

if debug: print "Found: ", essids_found
essids_known = scan_wpasupplicant()

if debug: print "Known: ", essids_known

if len(set(essids_found).intersection(set(essids_known))): print "wlan0-known"
else:     print "wlan0-host"
