# Pump Alarm 
# Nigel Armstrong June 2022
# v0.1
#
# Programme to sound an alarm if pump is left running longer than a certain time
#
from time import sleep   
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, initial=0) # pump 
GPIO.setup(24, GPIO.OUT, initial=0) # alarm buzzer

try:
    while False:        # while pump if off; set buzzer to off
        if GPIO.input(4):
            GPIO.output(24,0)
    else:               # when pump is on - wait ?? and then turn on alarm buzzer
        sleep(420)
            GPIO.output(24,1)
finally:
   GPIO.cleanup()       # cleans up GPIO 
