# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple seesaw test reading and writing the internal EEPROM
# The ATtiny8xx series has a true 128 byte EEPROM, the SAMD09 mimics it in flash with 64 bytes
# THE LAST BYTE IS USED FOR I2C ADDRESS CHANGE!
#
# See the seesaw Learn Guide for wiring details:
# https://learn.adafruit.com/adafruit-seesaw-atsamd09-breakout?view=all#circuitpython-wiring-and-test

import time
import board
from adafruit_seesaw import seesaw

i2c_bus = board.I2C()
ss = seesaw.Seesaw(i2c_bus)

val = ss.eeprom_read8(0x02)  # read from address 2
print("Read 0x%02x from EEPROM address 0x02" % val)

print("Incremening value")
ss.eeprom_write8(0x02, val + 1)

val = ss.eeprom_read8(0x02)  # read from address 2
print("Second read 0x%02x from EEPROM address 0x02" % val)

while True:
    # Do not write EEPROM in a loop, it has 100k cycle life
    time.sleep(1)
