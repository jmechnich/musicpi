#!/usr/bin/env python

import RPi.GPIO as GPIO
import os, sys, time, atexit, signal, subprocess

def blink():
        for i in xrange(2):
                GPIO.output(22, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(22, GPIO.LOW)
                time.sleep(0.2)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(22,GPIO.OUT)
atexit.register(GPIO.cleanup)
signal.signal(signal.SIGINT,lambda x, y: sys.exit(0))

while True:
        if GPIO.input(17) == 0:
                blink()
                GPIO.output(22, GPIO.HIGH)
                subprocess.call(["shutdown", "-h", "now"])
                break
	time.sleep(1)
