# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple seesaw test writing NeoPixels
# Can use any valid GPIO pin, up to 60 pixels!
#
# See the seesaw Learn Guide for wiring details:
# https://learn.adafruit.com/adafruit-seesaw-atsamd09-breakout?view=all#circuitpython-wiring-and-test

import time
import board
from rainbowio import colorwheel
from adafruit_seesaw import seesaw, neopixel

i2c_bus = board.I2C()
ss = seesaw.Seesaw(i2c_bus)

NEOPIXEL_PIN = 6  # change to any pin
NEOPIXEL_NUM = 30  # no more than 60!
pixels = neopixel.NeoPixel(ss, NEOPIXEL_PIN, NEOPIXEL_NUM)
pixels.brightness = 0.3  # not so brite!

color_offset = 0  # start at red

# cycle through all colors along the strip
while True:
    for i in range(NEOPIXEL_NUM):
        rc_index = (i * 256 // NEOPIXEL_NUM) + color_offset
        pixels[i] = colorwheel(rc_index & 255)
    pixels.show()
    color_offset += 1
    time.sleep(0.01)
