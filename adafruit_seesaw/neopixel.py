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

_NEOPIXEL_STATUS = const(0x00)
_NEOPIXEL_PIN = const(0x01)
_NEOPIXEL_SPEED = const(0x02)
_NEOPIXEL_BUF_LENGTH = const(0x03)
_NEOPIXEL_BUF = const(0x04)
_NEOPIXEL_SHOW = const(0x05)

class Neopixel:
    def __init__(self, seesaw, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):
        self._seesaw = seesaw
        self._pin = pin
        self._bpp = bpp
        self._auto_write = auto_write
        self._pixel_order = pixel_order
        self._n = n
        self._brightness = brightness

        cmd = bytearray([pin])
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_PIN, cmd)
        cmd = struct.pack(">H", n*self._bpp)
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF_LENGTH, cmd)

    @property
    def brightness(self):
        pass

    @brightness.setter
    def brightness(self, value):
        pass

    def deinit(self):
        pass

    def __len__(self):
        return self._n

    def __setitem__(self, key, value):
        cmd = bytearray(6)
        cmd[:2] = struct.pack(">H", key * self._bpp)
        cmd[2:] = struct.pack(">I", value)
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF, cmd)
        if self._auto_write:
            self.show()

    def __getitem__(self, key):
        pass

    def fill(self, color):
        cmd = bytearray(self._n*self._bpp+2)
        for i in range(self._n):
            cmd[self._bpp*i+2:] = struct.pack(">I", color)

        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF, cmd)

        if self._auto_write:
            self.show()

    def show(self):
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_SHOW)