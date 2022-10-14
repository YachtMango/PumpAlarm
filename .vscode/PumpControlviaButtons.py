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
fontM1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
fontM2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
size_x, size_y = draw.textsize(MESSAGE1, fontM1)
text_x = 160
text_y = (80 - size_y) // 2
t_start = time.time()

while True:
    x = (time.time() - t_start) * 100
    x %= (size_x + 160)
    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
    draw.text((int(text_x - x), text_y), MESSAGE1, font=fontM1, fill=(255, 255, 0))
    disp.display(img)
    while ahm.input.one.is_on():
            GPIO.output(25,1) # Ensure backlight is on
            ctemp = vcgm.measure_temp() 
            with open(LOG_FILE,'a') as l:
                l.write(datetime.now().strftime("%a %d/%m/%Y, %H:%M") + " Runtime " + str(INPUTA) + " Input Volts " + str(ahm.analog.one.read())  + " CPU Temp = " + str(ctemp) + " °C" "\n")
            ahm.relay.one.on() # 
            for i in reversed(range(1,INPUTA)):
                    time.sleep(1 - time.time() % 1)
                    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
                    draw.text((5,1), f"Pump runs \nfor {i} \nseconds", font=fontM2, fill=(0, 255, 255))
                    disp.display(img)
            ahm.relay.one.off()
    while ahm.input.two.is_on(): 
            GPIO.output(25,1) # Ensure backlight is on
            ctemp = vcgm.measure_temp()
            with open(LOG_FILE,'a') as l:
                l.write(datetime.now().strftime("%a %d/%m/%Y, %H:%M") + " Runtime " + str(INPUTB) + " Input Volts " + str(ahm.analog.one.read())  + " CPU Temp = " + str(ctemp) + " °C" "\n")
            ahm.relay.one.on()  # 
            for i in reversed(range(1,INPUTB)):
                    time.sleep(1 - time.time() % 1)
                    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
                    draw.text((5,1), f"Pump runs \nfor {i} \nseconds", font=fontM2, fill=(255, 0, 255))
                    disp.display(img)
            ahm.relay.one.off()