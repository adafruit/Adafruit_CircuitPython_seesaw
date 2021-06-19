# SPDX-FileCopyrightText: 2021 Greg Paris for Adafruit Industries
# SPDX-License-Identifier: MIT
"""Test of a single NeoKey_1x4 module"""

from time import sleep
import board
from adafruit_seesaw.neokey_1x4 import NeoKey_1x4

i2c = board.I2C()
nk = NeoKey_1x4(i2c)

color = (0xFF0000, 0x00FF00, 0x0000FF, 0xFF6600)


def test(event):
    if event.action == NeoKey_1x4.RELEASED:
        event.obj[event.key] = 0
    elif event.action == NeoKey_1x4.PRESSED:
        event.obj[event.key] = color[event.key]
    print("got {} {}".format(event.key, event.action))


for i in range(4):
    nk.register_callback(i, test)

while True:
    pressed, just_pressed, just_released = nk.read_keys()
    print(pressed, just_pressed, just_released)
    sleep(0.2)
