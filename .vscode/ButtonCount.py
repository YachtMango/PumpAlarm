#!/usr/bin/env python3

InputA = 3
InputB = 6
InputC = 9

import sys
from time import sleep
import threading
import automationhat
sleep(0.1) # Short pause after ads1015 class creation recommended

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

import ST7735 as ST7735

print("""input.py

Bla Bla

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

    # Values to keep everything aligned nicely.
    on_x = 115
    on_y = 35

    off_x = 46
    off_y = on_y

    dia = 10

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

def Buttons():
    bcount = 0	# initialize count
    while True:        #          
        if automationhat.input.two.is_on():
            (bcount) += 1
            print (bcount), sleep(.3)
            while True:        #          
                if (bcount)== 1:
                    automationhat.relay.one.on()
                    print("Runs for", (InputA), "seconds")
                    sleep(InputA)
                    automationhat.relay.one.off()
                elif (bcount) == 2:  
                    automationhat.relay.one.on() 
                    print ("Runs for", (InputB), "seconds")
                    sleep(InputB)
                    automationhat.relay.one.off()
                elif (bcount) == 3: 
                    automationhat.relay.one.on() 
                    print ("Runs for", (InputC), "seconds")
                    sleep(InputC)
                    automationhat.relay.one.off()
                else: 
                    (bcount) == 0
                    print("counter reset - try again")
                    automationhat.relay.one.off()
        else:
            automationhat.relay.one.off()

           
thread1 = threading.Thread(target=LCD)
thread1.start()

thread2 = threading.Thread(target=Buttons)
thread2.start()