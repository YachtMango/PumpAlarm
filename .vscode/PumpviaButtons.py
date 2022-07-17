#!/usr/bin/env python3
# Pump Alarm via AutomationHat and Buttons
# Nigel Armstrong July 2022
# v0.1
#
# Programme to contorl pump when buttons are pressed
#
InputA = 6
InputB = 9
InputC = 15

import sys
from time import sleep 
import threading
import automationhat
sleep(0.1) # Short pause after ads1015 class creation recommended

try:
    from PIL import Image, ImageFont, ImageDraw
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

import ST7735 as ST7735

try:
    from fonts.ttf import RobotoBlackItalic as UserFont
except ImportError:
    print("""This example requires the Roboto font.
Install with: sudo pip{v} install fonts font-roboto
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

print("""PumpviaButtons.py

When Button 1 is pressed pump ( relay 1) runs for X seconds:
When Button 2 is pressed pumps runs for Y seconds.

Press CTRL+C to exit.
""")

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

# Values to keep everything aligned nicely.
on_x = 115
on_y = 35

off_x = 46
off_y = on_y

dia = 10

def dispvalue():
    while True:
    # Value to increment for spacing circles vertically.
        offset = 0

    # Open our background image.
        image = Image.open("images/inputs-blank.jpg")
        draw = ImageDraw.Draw(image)

    # Draw the circle for each channel in turn.
        for channel in range(3):
            if automationhat.input[channel].is_on():
                draw.ellipse((on_x, on_y + offset, on_x + dia, on_y + dia + offset), on_colour)
            elif automationhat.input[channel].is_off():
                draw.ellipse((off_x, off_y + offset, off_x + dia, off_y + dia + offset), off_colour)

        offset += 14

    # Draw the image to the display
        disp.display(image)

        sleep(0.25)

def buttons():   
    while True:        #          
        if automationhat.input.one.is_off() or automationhat.input.two.is_off():
                automationhat.relay.one.off()
        elif automationhat.input.one.on():  
            automationhat.relay.one.on() # when Input 1 is High the run pump for sleep time A
            sleep(InputA)
        elif automationhat.input.two.on(): 
            automationhat.relay.one.on()  # when Input 2 is High the run pump for sleep time B
            sleep(InputB)
        elif automationhat.input.one.on() and automationhat.input.two.on():
            automationhat.relay.one.on()  # when input 1 and 2  is High the run pump for sleep time C
            sleep(InputC)
    
thread1 = threading.Thread(target=dispvalue)
thread1.start()

thread2 = threading.Thread(target=buttons)
thread2.start()