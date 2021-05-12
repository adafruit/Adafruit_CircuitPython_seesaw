# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

import board
import busio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO

i2c_bus = busio.I2C(board.SCL, board.SDA)

seesaw = Seesaw(i2c_bus, addr=0x36)

button = DigitalIO(seesaw, 24)
button_held = False

last_position = seesaw.encoder_position()

while True:

    # read position of the rotary encoder
    position = seesaw.encoder_position()
    if position != last_position:
        last_position = position
        print("Position: {}".format(position))

    if not button.value and not button_held:
        button_held = True
        print("Button pressed")

    if button.value and button_held:
        button_held = False
        print("Button released")
