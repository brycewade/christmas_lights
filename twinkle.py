#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
import random
import datetime

# LED strip configuration:
LED_COUNT      = 148      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def setTwinkle(strip, status, i):
    now = datetime.datetime.now()
    difference = now - status['start']
    elapsed = difference.total_seconds() * 1000
#    print('In setTwinkle: {} {} {}'.format(i,elapsed,status))
    if elapsed < 500:
        red=int(status['red'] * elapsed / 500)
        green=int(status['green'] * elapsed / 500)
        blue=int(status['blue'] * elapsed / 500)
        color = Color(red, blue, green)
#        print('Ramping up {} to {},{},{}'.format(i,red,blue,green))
        strip.setPixelColor(i, color)
        return status['start']
    elif elapsed < 1000:
        red=int(status['red'] * (1000 - elapsed) / 500)
        green=int(status['green'] * (1000 - elapsed) / 500)
        blue=int(status['blue'] * (1000 - elapsed) / 500)
        color = Color(red, blue, green)
#        print('Ramping Down {} to {},{},{}'.format(i,red,blue,green))
        strip.setPixelColor(i, color)
        return status['start']
    else:
#        print("Turning off {}".format(i))
        color = Color(0, 0, 0)
        strip.setPixelColor(i, color)
        return 0

def twinkle(strip, wait_ms=50, percent_on=5):
    status = [ {'start': 0} ] * strip.numPixels()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
        status[i] = {'start': 0}
    strip.show()
    while True:
        for i in range(strip.numPixels()):
            if status[i]['start'] == 0:
                rand = random.randint(0,wait_ms*100)
#                print('{},{}'.format(i,rand))
                if rand < percent_on:
                    status[i]['red'] = random.randint(0,256)
                    status[i]['green'] = random.randint(0,256)
                    status[i]['blue'] = random.randint(0,256)
                    status[i]['start'] = datetime.datetime.now()
            else:
                status[i]['start'] = setTwinkle(strip, status[i], i)
        strip.show()
        time.sleep(wait_ms/1000.0)
    

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-n', '--noselftest', action='store_true', help='clear the display on exit')
    parser.add_argument('-l', '--leds', default=LED_COUNT, help='set the number of LEDs in the strip')
    parser.add_argument('-p', '--probability', default=5, help='set the probability of each LED being on')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(int(args.leds), LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        if not args.noselftest:
# Self test
            print ('Color wipe animations.')
            colorWipe(strip, Color(255, 0, 0))  # Red wipe
            colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            colorWipe(strip, Color(0, 0, 255))  # Green wipe
            print ('Theater chase animations.')
            theaterChase(strip, Color(127, 127, 127))  # White theater chase
            theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
#            print ('Rainbow animations.')
#            rainbow(strip)
#            rainbowCycle(strip)
#            theaterChaseRainbow(strip)
# Main twinkle loop
        while True:
            twinkle(strip, 50, float(args.probability))

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
