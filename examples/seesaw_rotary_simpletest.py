# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

import board
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.rotaryio import IncrementalEncoder

i2c_bus = board.I2C()

seesaw = Seesaw(i2c_bus, addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

button = DigitalIO(seesaw, 24)
button_held = False

encoder = IncrementalEncoder(seesaw)
last_position = None

while True:

    # read position of the rotary encoder
    position = encoder.position
    if position != last_position:
        last_position = position
        print("Position: {}".format(position))

    if not button.value and not button_held:
        button_held = True
        print("Button pressed")

    if button.value and button_held:
        button_held = False
        print("Button released")
