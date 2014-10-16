#!/usr/bin/env python

import RPi.GPIO as GPIO
import os, time, atexit, signal

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)
atexit.register(GPIO.cleanup)
signal.signal(signal.SIGINT,GPIO.cleanup)

for i in xrange(3):
    GPIO.output(22, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(22, GPIO.LOW)
    time.sleep(0.2)
