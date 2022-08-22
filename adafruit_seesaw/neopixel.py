# SPDX-FileCopyrightText: 2017 Dean Miller for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# pylint: disable=missing-docstring,invalid-name,too-many-public-methods

"""
`adafruit_seesaw.neopixel`
====================================================
"""
import struct
from adafruit_pixelbuf import PixelBuf

try:
    from micropython import const
except ImportError:

    def const(x):
        return x


### hack to make sure this module is not placed in root CIRCUITPY/lib folder
if "." not in __name__:
    raise ImportError(
        "seesaw neopixel being imported from unexpected location - is seesaw neopixel use intended?"
    )

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"

_NEOPIXEL_BASE = const(0x0E)

_NEOPIXEL_STATUS = const(0x00)
_NEOPIXEL_PIN = const(0x01)
_NEOPIXEL_SPEED = const(0x02)
_NEOPIXEL_BUF_LENGTH = const(0x03)
_NEOPIXEL_BUF = const(0x04)
_NEOPIXEL_SHOW = const(0x05)

# try lower values if IO errors
_OUTPUT_BUFFER_SIZE = const(24)

# Pixel color order constants
RGB = "RGB"
"""Red Green Blue"""
GRB = "GRB"
"""Green Red Blue"""
RGBW = "RGBW"
"""Red Green Blue White"""
GRBW = "GRBW"
"""Green Red Blue White"""


class NeoPixel(PixelBuf):
    """Control NeoPixels connected to a seesaw

    :param ~adafruit_seesaw.seesaw.Seesaw seesaw: The device
    :param int pin: The pin number on the device
    :param int n: The number of pixels
    :param int bpp: The number of bytes per pixel
    :param float brightness: The brightness, from 0.0 to 1.0
    :param bool auto_write: Automatically update the pixels when changed
    :param tuple pixel_order: The layout of the pixels.
        Use one of the order constants such as RGBW."""

    def __init__(
        self,
        seesaw,
        pin,
        n,
        *,
        bpp=None,
        brightness=1.0,
        auto_write=True,
        pixel_order="GRB"
    ):
        self._seesaw = seesaw
        self._pin = pin
        if not pixel_order:
            pixel_order = GRB if bpp == 3 else GRBW
        elif isinstance(pixel_order, tuple):
            # convert legacy pixel order into PixelBuf pixel order
            order_list = ["RGBW"[order] for order in pixel_order]
            pixel_order = "".join(order_list)

        super().__init__(
            n,
            byteorder=pixel_order,
            brightness=brightness,
            auto_write=auto_write,
        )

        cmd = bytearray([pin])
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_PIN, cmd)
        cmd = struct.pack(">H", n * self.bpp)
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF_LENGTH, cmd)
        self.output_buffer = bytearray(_OUTPUT_BUFFER_SIZE)

    def _transmit(self, buffer: bytearray) -> None:
        """Update the pixels even if auto_write is False"""

        step = _OUTPUT_BUFFER_SIZE - 2
        for i in range(0, len(buffer), step):
            self.output_buffer[0:2] = struct.pack(">H", i)
            self.output_buffer[2:] = buffer[i : i + step]
            self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF, self.output_buffer)

        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_SHOW)

    def deinit(self):
        pass
