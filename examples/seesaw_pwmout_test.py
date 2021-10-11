# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple seesaw test for writing PWM outputs
# On the SAMD09 breakout these are pins 5, 6, and 7
# On the ATtiny8x7 breakout these are pins 0, 1, 9, 12, 13
#
# See the seesaw Learn Guide for wiring details:
# https://learn.adafruit.com/adafruit-seesaw-atsamd09-breakout?view=all#circuitpython-wiring-and-test

import time
import board
from adafruit_seesaw import seesaw, pwmout

i2c_bus = board.I2C()
ss = seesaw.Seesaw(i2c_bus)

PWM_PIN = 9  # change to a valid PWM output!
pwm = pwmout.PWMOut(ss, PWM_PIN)

while True:
    # the API PWM range is 0 to 65535, but we increment by 256 since our
    # resolution is often only 8 bits underneath
    pwm.duty_cycle = (pwm.duty_cycle + 256) % 65536
    time.sleep(0.01)
