#!/usr/bin/env python3
# Pump control via AutomationHat and Buttons
# Nigel Armstrong Nov 2022
# v4
#
# Programme to control pump when buttons are pressed and display oump run time, CPU, Internal and External temperatures
#
#INPUTA = 300  # 3.5 mins  = 210
#INPUTB = 600  # 7.5 mins  = 450
#LOG_FILE = "/home/pi/Pimoroni/automationhat/examples/hat-mini/pumplogfile.txt"
INPUTA = 13  # 3.5 mins  = 210
INPUTB = 16  # 7.5 mins  = 450
LOG_FILE = "/home/pump/pumplogfile.txt"
MESSAGE1 = "Press I or II to run the pump !"
EXTTEMPID = '0b228128f0d0'
INTTEMPID = '0315034334ff'

from datetime import datetime
import time 
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoBlackItalic as UserFont
import automationhat as ahm
import ST7735 as ST7735
from vcgencmd import Vcgencmd
vcgm = Vcgencmd()
from w1thermsensor import W1ThermSensor
time.sleep(0.1) # Short pause after ads1015 class creation recommended
extemp = W1ThermSensor(sensor_id=EXTTEMPID)
intemp = W1ThermSensor(sensor_id=INTTEMPID)


def Backlight():
    if ahm.input.three.is_off():  # check input from microbit light sensor
        ahm.GPIO.output(25,1)
    else:
        ahm.GPIO.output(25,0)


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
fontM1 = ImageFont.truetype(UserFont, 38)
fontM2 = ImageFont.truetype(UserFont, 20)
size_x, size_y = draw.textsize(MESSAGE1, fontM1)
text_x = 160
text_y = (80 - size_y) // 2
t_start = time.time()


while True:     # code to display scolling text
    x = (time.time() - t_start) * 100
    x %= (size_x + 160)
    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
    draw.text((int(text_x - x), text_y), MESSAGE1, font=fontM1, fill=(255, 255, 0))
    disp.display(img)
    Backlight() # check light level and turn on/off backlight whilst MESSAGE1 is shown.
    while ahm.input.one.is_on():
            ahm.GPIO.output(25,1) # Ensure backlight is on 
            ctemp = vcgm.measure_temp() # CPU temp
            etemp = extemp.get_temperature() # external temp
            itemp = intemp.get_temperature() # internal temp
            with open(LOG_FILE,'a') as l:
                l.write(str(time.time()) + "," + str(INPUTA) + "," + str(ahm.analog.one.read())  + "," + str(ctemp) + "," + str(itemp) + "," + str(etemp) + "\n")
            ahm.relay.one.on() # turns pump on
            for i in reversed(range(1,INPUTA)):
                    time.sleep(1 - time.time() % 1)
                    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
#                    draw.text((0,5),str(" Ext ="  + str(etemp)),font=fontM2, fill=(255, 0, 255))
#                    draw.text((0,20),str(" Int = " + str(itemp)), font=fontM2, fill=(255, 0, 255))
#                    draw.text((0,40),str("CPU = " + str(ctemp)), font=fontM2, fill=(255, 0, 255))
                    draw.text((10,1), f"Pump runs \nfor {i} \nseconds", font=fontM2, fill=(0, 255, 255))
                    disp.display(img)
            ahm.relay.one.off() # turns pump off
    while ahm.input.two.is_on(): 
            ahm.GPIO.output(25,1) # Ensure backlight is on 
            ctemp = vcgm.measure_temp()
            etemp = extemp.get_temperature() # external temp
            itemp = intemp.get_temperature() # internal temp
            with open(LOG_FILE,'a') as l:
                l.write(str(time.time()) + "," + str(INPUTB) + "," + str(ahm.analog.one.read())  + "," + str(ctemp) + "," + str(itemp) + "," + str(etemp) + "\n")
            ahm.relay.one.on()  # 
            for i in reversed(range(1,INPUTB)):
                    time.sleep(1 - time.time() % 1)
                    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
                    draw.text((5,1), f"Pump runs \nfor {i} \nseconds", font=fontM2, fill=(255, 0, 255))
                    disp.display(img)
            ahm.relay.one.off() # turns pump off