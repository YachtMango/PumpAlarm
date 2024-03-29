#!/usr/bin/env python3
# Pump control via AutomationHat and Buttons
# Nigel Armstrong July 2022
# 
#
# Programme to control pump when buttons are pressed
#
INPUTA = 300  # 3.5 mins  = 210
INPUTB = 600  # 7.5 mins  = 450
IMAGE_FILE = "/home/pi/Pimoroni/automationhat/examples/hat-mini/images/PumpImage.jpg"
LOG_FILE = "/home/pi/Pimoroni/automationhat/examples/hat-mini/pumplogfile.txt"


from datetime import datetime
import sys
from time import sleep
import threading
import automationhat as ahm
import RPi.GPIO as GPIO
import ST7735 as ST7735
from vcgencmd import Vcgencmd
vcgm = Vcgencmd()

sleep(0.1) # Short pause after ads1015 class creation recommended

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

try:
    from fonts.ttf import RobotoBlackItalic as UserFont
except ImportError:
    print("""This example requires the Roboto font.
Install with: sudo pip{v} install fonts font-roboto
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

print("""PumpviaButtons.py

Programme to run pump via relay on Automation Hat mini based for a duration depending on
which input button is pressed.

Press CTRL+C to exit.
""")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25, GPIO.OUT)

def LCD():
    # Create ST7735 LCD display class.
    disp = ST7735.ST7735(
        port=0,
        cs=ST7735.BG_SPI_CS_FRONT,
        dc=9,
        backlight=25,
        rotation=270,
        spi_speed_hz=4000000
    )

    # Initialize display.
    disp.begin()

    on_colour = (99, 225, 162)
    off_colour = (235, 102, 121)
    tfont = ImageFont.truetype(UserFont, 16)
    colour = (255, 181, 86)

    # Values to keep everything aligned nicely.
    on_x = 115
    on_y = 35

    off_x = 46
    off_y = on_y

    dia = 10

    text_x = 30
    text_y = 34

    while True:
        # Value to increment for spacing circles vertically.
        offset = 0

        # Open our background image.
        image = Image.open(IMAGE_FILE)
        draw = ImageDraw.Draw(image)

        # Draw the circle for each channel in turn.
        for channel in range(2):
            if ahm.input[channel].is_on():
                draw.ellipse((on_x, on_y + offset, on_x + dia, on_y + dia + offset), on_colour)
            elif ahm.input[channel].is_off():
                draw.ellipse((off_x, off_y + offset, off_x + dia, off_y + dia + offset), off_colour)

            offset += 14
        if ahm.relay.one.is_on():
            draw.text((text_x, text_y + offset), text="Pump is running", font=tfont, fill=colour)

        # Draw the image to the display
        disp.display(image)

        sleep(0.25)

def Buttons():
    while True:          
        if ahm.input.one.is_on(): 
            ctemp = vcgm.measure_temp()
            GPIO.output(25,1) # Ensure backlight is on 
            ahm.relay.one.on() # when Input 1 is High the run pump for sleep time A
            with open(LOG_FILE,'a') as l:
                l.write(datetime.now().strftime("%a %d/%m/%Y, %H:%M") + " Runtime " + str(INPUTA) + " Input Volts " + str(ahm.analog.one.read())  + " CPU Temp = " + str(ctemp) + " °C" "\n")
            sleep(INPUTA)
            ahm.relay.one.off()
        elif ahm.input.two.is_on():
            ctemp = vcgm.measure_temp() 
            GPIO.output(25,1) # Ensure backlight is on
            ahm.relay.one.on()  # when Input 2 is High the run pump for sleep time B
            with open(LOG_FILE,'a') as l:
                l.write(datetime.now().strftime("%a %d/%m/%Y, %H:%M") + " Runtime " + str(INPUTB) + " Input Volts " + str(ahm.analog.one.read())  + " CPU Temp = " + str(ctemp) + " °C" "\n")
            sleep(INPUTB)
            ahm.relay.one.off()
        sleep(0.2) # Reduce CPU time

def Backlight():
    while True:
        if ahm.input.three.is_off():
            GPIO.output(25,1)
        else:
           GPIO.output(25,0)
        sleep (5)

thread1 = threading.Thread(target=LCD)
thread1.start()

thread2 = threading.Thread(target=Buttons)
thread2.start()

thread3 = threading.Thread(target=Backlight)
thread3.start()