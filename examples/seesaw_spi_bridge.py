# SPDX-FileCopyrightText: 2026 Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Experimental C011 SPI bridge: connect PA7/MOSI to PA6/MISO for loopback.

Requires SPI-enabled peripheral firmware. PA4 is CS and PA5 is SCK.
Do not connect another device's output to the loopback wire.
This is not a drop-in busio.SPI display driver.
"""

import board

from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.spi import SPIBridge

print("Adafruit seesaw STM32C011 SPI bridge")
seesaw = Seesaw(board.I2C(), addr=0x49)
spi = SPIBridge(seesaw)

try:
    spi.configure(frequency=1000000, mode=0)
    print("SPI clock:", spi.clock_frequency, "Hz")
    message = b"Hello through the seesaw SPI bridge!"
    received = bytearray(len(message))
    spi.transfer(message, received)
    print("Sent:", message)
    print("Received:", received)
finally:
    spi.abort()
