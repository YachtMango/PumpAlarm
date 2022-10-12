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
MESSAGE2 = "Pump running for "

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

img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
size_x, size_y = draw.textsize(MESSAGE, font)
text_x = 160
text_y = (80 - size_y) // 2

t_start = time.time()

while True:
    x = (time.time() - t_start) * 100
    x %= (size_x + 160)
    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
    draw.text((int(text_x - x), text_y), MESSAGE1, font=font, fill=(255, 255, 255))
    disp.display(img)