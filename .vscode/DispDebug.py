#!/usr/bin/env python3
# Pump control via AutomationHat and Buttons
# Nigel Armstrong July 2022
# v0.1
#
# Programme to control pump when buttons are pressed
#
InputA = 3
InputB = 6
InputC = 9
MESSTXT = "Pump runs" ,(InputA), "seconds"

from datetime import datetime
import sys
from time import sleep
import threading
import automationhat

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

import ST7735 as ST7735

print("""DispDebug.py

Programme to debug the ST7735 display

Press CTRL+C to exit.
""")

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
    tfont = ImageFont.truetype(UserFont, 12)
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
        image = Image.open("images/inputs-blank.jpg")
        draw = ImageDraw.Draw(image)

        # Draw the circle for each channel in turn.
        for channel in range(2):
            if automationhat.input[channel].is_on():
                draw.ellipse((on_x, on_y + offset, on_x + dia, on_y + dia + offset), on_colour)
            elif automationhat.input[channel].is_off():
                draw.ellipse((off_x, off_y + offset, off_x + dia, off_y + dia + offset), off_colour)

            offset += 14
        if automationhat.relay.one.is_on():
            draw.text((text_x, text_y + offset), text="Pump running ", font=tfont, fill=colour)

        # Draw the image to the display
        disp.display(image)

        sleep(0.25)

def Buttons():
    while True:        #          
        if automationhat.input.one.is_on():  
            automationhat.relay.one.on() # when Input 1 is High the run pump for sleep time A
            # with open('pumplogfile.txt','a') as l:
            #    l.write(datetime.now().strftime("%c") + "\n")
            print ("Input 1" ,(InputA), "seconds")
            sleep(InputA)
            automationhat.relay.one.off()
        elif automationhat.input.two.is_on(): 
            automationhat.relay.one.on()  # when Input 2 is High the run pump for sleep time B
            print ("Input 2", (InputB), "seconds")
            #with open('pumplogfile.txt','a') as l:
            #    l.write(datetime.now().strftime("%c") + "\n")
            sleep(InputB)
            automationhat.relay.one.off()

thread1 = threading.Thread(target=LCD)
thread1.start()

thread2 = threading.Thread(target=Buttons)
thread2.start()