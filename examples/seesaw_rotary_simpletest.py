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

last_pos = seesaw.get_encoder_pos()

while True:

    # read position of the rotary encoder
    pos = seesaw.get_encoder_pos()
    if pos != last_pos:
        last_pos = pos
        print(f"Position: {pos}")

    if not button.value and not button_held:
        button_held = True
        print("Button pressed")

    if button.value and button_held:
        button_held = False
        print("Button released")
