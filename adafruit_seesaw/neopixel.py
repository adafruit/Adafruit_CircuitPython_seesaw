# The MIT License (MIT)
#
# Copyright (c) 2017 Dean Miller for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# pylint: disable=missing-docstring,invalid-name,too-many-public-methods

try:
    import struct
except ImportError:
    import ustruct as struct
from micropython import const

__version__ = "1.2.3"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"

_NEOPIXEL_BASE = const(0x0E)

_NEOPIXEL_STATUS = const(0x00)
_NEOPIXEL_PIN = const(0x01)
_NEOPIXEL_SPEED = const(0x02)
_NEOPIXEL_BUF_LENGTH = const(0x03)
_NEOPIXEL_BUF = const(0x04)
_NEOPIXEL_SHOW = const(0x05)

# Pixel color order constants
RGB = (0, 1, 2)
"""Red Green Blue"""
GRB = (1, 0, 2)
"""Green Red Blue"""
RGBW = (0, 1, 2, 3)
"""Red Green Blue White"""
GRBW = (1, 0, 2, 3)
"""Green Red Blue White"""

class NeoPixel:
    def __init__(self, seesaw, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):
        # TODO: brightness not yet implemented.
        self._seesaw = seesaw
        self._pin = pin
        self._bpp = bpp
        self.auto_write = auto_write
        self._n = n
        self._brightness = min(max(brightness, 0.0), 1.0)
        self._pixel_order = GRBW if pixel_order is None else pixel_order

        cmd = bytearray([pin])
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_PIN, cmd)
        cmd = struct.pack(">H", n*self._bpp)
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF_LENGTH, cmd)

    @property
    def brightness(self):
        """Overall brightness of the pixel"""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        # pylint: disable=attribute-defined-outside-init
        self._brightness = min(max(brightness, 0.0), 1.0)
        if self.auto_write:
            self.show()

    def deinit(self):
        pass

    def __len__(self):
        return self._n

    def __setitem__(self, key, color):
        cmd = bytearray(2 + self._bpp)
        struct.pack_into(">H", cmd, 0, key * self._bpp)
        if isinstance(color, int):
            w = color >> 24
            r = (color >> 16) & 0xff
            g = (color >> 8) & 0xff
            b = color & 0xff
        else:
            if self._bpp == 3:
                r, g, b = color
            else:
                r, g, b, w = color

        # If all components are the same and we have a white pixel then use it
        # instead of the individual components.
        if self._bpp == 4 and r == g == b:
            w = r
            r = 0
            g = 0
            b = 0

        if self.brightness < 0.99:
            r = int(r * self.brightness)
            g = int(g * self.brightness)
            b = int(b * self.brightness)
            if self._bpp == 4:
                w = int(w * self.brightness)

        # Store colors in correct slots
        cmd[2 + self._pixel_order[0]] = r
        cmd[2 + self._pixel_order[1]] = g
        cmd[2 + self._pixel_order[2]] = b
        if self._bpp == 4:
            cmd[2 + self._pixel_order[3]] = w

        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF, cmd)
        if self.auto_write:
            self.show()

    def __getitem__(self, key):
        pass

    def fill(self, color):
        # Suppress auto_write while filling.
        current_auto_write = self.auto_write
        self.auto_write = False
        for i in range(self._n):
            self[i] = color
        if current_auto_write:
            self.show()
        self.auto_write = current_auto_write

    def show(self):
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_SHOW)
