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
pump_run_timer = 180 # run time before alarm

try:
    while False:        # while pump is off; set buzzer to off
        if GPIO.input(4):
            GPIO.output(24,0)
        else:               # when pump is on - wait ?? and then turn on alarm buzzer
            sleep(pump_run_timer)
            GPIO.output(24,1)
        sleep(1)            # wait 1 second

finally:
   GPIO.cleanup()       # cleans up GPIO 
