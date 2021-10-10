# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple seesaw test reading analog value
# on SAMD09, analog in can be pins 2, 3, or 4
# on Attiny8x7, analog in can be pins 0, 1, 2, 3, 6, 7, 18, 19, 20
#
# See the seesaw Learn Guide for wiring details:
# https://learn.adafruit.com/adafruit-seesaw-atsamd09-breakout?view=all#circuitpython-wiring-and-test

import time
import board
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.analoginput import AnalogInput

i2c_bus = board.I2C()
ss = Seesaw(i2c_bus)

analogin_pin = 2
analog_in = AnalogInput(ss, analogin_pin)

while True:
    print(analog_in.value)
    time.sleep(0.1)
