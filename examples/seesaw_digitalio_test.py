# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple seesaw test using an LED attached to Pin 5 and a button on pin 2
#
# See the seesaw Learn Guide for wiring details:
# https://learn.adafruit.com/adafruit-seesaw-atsamd09-breakout?view=all#circuitpython-wiring-and-test

import time
import board
import digitalio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO

i2c_bus = board.I2C()
ss = Seesaw(i2c_bus)

button_pin = 2
led_pin = 5

button = DigitalIO(ss, button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led = DigitalIO(ss, led_pin)
led.direction = digitalio.Direction.OUTPUT

while True:
    # simply set the LED to the same 'value' as the button pin
    led.value = button.value
    time.sleep(0.1)
