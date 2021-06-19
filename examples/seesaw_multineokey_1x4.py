# SPDX-FileCopyrightText: 2021 Greg Paris for Adafruit Industries
# SPDX-License-Identifier: MIT
"""Test of multiple NeoKey_1x4 modules"""

from time import sleep
import board
from adafruit_seesaw.neokey_1x4 import NeoKey_1x4, MultiNeoKey_1x4

# example vertical orientation of two modules
i2c_addrs = (
    (0x30,),
    (0x31,),  # requires solder bridge
)
color = {
    (0, 0): 0xFF0000,
    (1, 0): 0x00FF00,
    (2, 0): 0x0000FF,
    (3, 0): 0xFF6600,
    (0, 1): 0xFF0066,
    (1, 1): 0x00FF66,
    (2, 1): 0x6600FF,
    (3, 1): 0xFFFFFF,
}

i2c = board.I2C()
mnk = MultiNeoKey_1x4(i2c, i2c_addrs)


def multitest(event):
    """Light the key a specific color when pressed"""
    if event.action == NeoKey_1x4.RELEASED:
        event.obj[event.key] = 0
    elif event.action == NeoKey_1x4.PRESSED:
        event.obj[event.key] = color[event.key]
    print("got {} {}".format(event.key, event.action))


for key in color.keys():
    mnk.register_callback(key, multitest)

while True:
    pressed, just_pressed, just_released = mnk.read_keys()
#   print(pressed, just_pressed, just_released)
#   sleep(0.2)
