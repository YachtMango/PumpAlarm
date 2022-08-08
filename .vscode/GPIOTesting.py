#!/usr/bin/env python3
# GPIO Testing
# Programme to test GPIO functions - Polling / Interrupts and Edge detection
# Nigel Armstrong July 2022
#
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

InputA = 240  # 3.5 mins  = 210
InputB = 480  # 7.5 mins  = 450

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.OUT)

print("""GPIOTesting.py

Programme to test GPIO functions - Polling / Interrupts and Edge detection

Press CTRL+C to exit.
""")

GPIO.add_event_detect(11, GPIO.FALLING, bouncetime=200) # wait for falling

try:
    while True: # wait for edge
        if GPIO.event_detected(11):
            print(datetime.now().strftime("%c") + " " + str(InputA))
            GPIO.output(13,1)
            sleep (3)
        else:
            GPIO.output(13,0)
        sleep(0.1)
except KeyboardInterrupt:
    print(" Ctrl-C - quit")
finally:
    GPIO.cleanup()