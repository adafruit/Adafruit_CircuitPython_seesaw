# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Simple seesaw test for ATtiny8x7 breakout using built-in LED on pin 5.
"""
import time
import board
from adafruit_seesaw.seesaw import Seesaw

ss = Seesaw(board.I2C())

ss.pin_mode(5, ss.OUTPUT)

while True:
    ss.digital_write(5, False)  # Turn the LED on (the built-in LED is active low!)
    time.sleep(1)  # Wait for one second
    ss.digital_write(5, True)  # Turn the LED off
    time.sleep(1)  # Wait for one second
