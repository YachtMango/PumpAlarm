#!/usr/bin/env python3
# Pump control via AutomationHat and Buttons
# Nigel Armstrong July 2022
# v0.1
#
# Programme to test and control LCD back light
#
from time import sleep
import automationhat as ahm
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25, GPIO.OUT)

print("""Backlighttest.py

Programme to control LCD back light

Press CTRL+C to exit.
""")
try:
    while True:
        #ahmi3 = ahm.input.three.read()
        #p25 = GPIO.output(25, not GPIO.input(25))
        if ahm.input.three.is_off():
            GPIO.output(25,1)
            #print (ahmi3)
            #print (p25)
        else:
            GPIO.output(25,0)
            #print (ahmi3)
            #print (p25)
        sleep (5)
except KeyboardInterrupt:
    print(" Ctrl-C - quit")
finally:
    GPIO.cleanup()