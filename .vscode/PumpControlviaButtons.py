#!/usr/bin/env python3
# Pump control via AutomationHat and Buttons
# Nigel Armstrong Oct 2022
# v2
#
# Programme to control pump when buttons are pressed
#
INPUTA = 3  # 3.5 mins  = 210
INPUTB = 6  # 7.5 mins  = 450
IMAGE_FILE = "/home/pi/PumpImage.jpg"
LOG_FILE = "/home/pi/pumplogfile.txt"
MESSAGE1 = "Press I or II to run the pump!"
MESSAGE2 = f"Pump runs for {INPUTA} secs"
MESSAGE3 = f"Pump runs for {INPUTB} secs"

from datetime import datetime
import sys
import time 
import threading
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import automationhat as ahm
import RPi.GPIO as GPIO
import ST7735 as ST7735
from vcgencmd import Vcgencmd
vcgm = Vcgencmd()

time.sleep(0.1) # Short pause after ads1015 class creation recommended


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

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
size_x, size_y = draw.textsize(MESSAGE1, font)
text_x = 160
text_y = (80 - size_y) // 2
t_start = time.time()

while True:
    x = (time.time() - t_start) * 100
    x %= (size_x + 160)
    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
    draw.text((int(text_x - x), text_y), MESSAGE1, font=font, fill=(255, 255, 255))
    disp.display(img)
    while ahm.input.one.is_on():
            GPIO.output(25,1) # Ensure backlight is on
            ctemp = vcgm.measure_temp() 
            ahm.relay.one.on() # when Input 1 is High the run pump for sleep time A
            draw.rectangle((0, 0, 160, 80), (0, 0, 0))
            draw.text((int(text_x - x), text_y), MESSAGE2, font=font, fill=(255, 255, 255))
            disp.display(img)
            with open(LOG_FILE,'a') as l:
                l.write(datetime.now().strftime("%a %d/%m/%Y, %H:%M") + " Runtime " + str(INPUTA) + " Input Volts " + str(ahm.analog.one.read())  + " CPU Temp = " + str(ctemp) + " °C" "\n")
            time.sleep(INPUTA)
            ahm.relay.one.off()
    while ahm.input.two.is_on():
            ctemp = vcgm.measure_temp() 
            GPIO.output(25,1) # Ensure backlight is on
            ahm.relay.one.on()  # when Input 2 is High the run pump for sleep time B
            draw.rectangle((0, 0, 160, 80), (0, 0, 0))
            draw.text((int(text_x - x), text_y), MESSAGE3, font=font, fill=(255, 255, 255))
            disp.display(img)
            with open(LOG_FILE,'a') as l:
                l.write(datetime.now().strftime("%a %d/%m/%Y, %H:%M") + " Runtime " + str(INPUTB) + " Input Volts " + str(ahm.analog.one.read())  + " CPU Temp = " + str(ctemp) + " °C" "\n")
            time.sleep(INPUTB)
            ahm.relay.one.off()