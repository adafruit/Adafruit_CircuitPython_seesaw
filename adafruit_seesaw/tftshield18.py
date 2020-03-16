# The MIT License (MIT)
#
# Copyright (c) 2018 Dean Miller for Adafruit Industries
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

"""
`adafruit_seesaw.tftshield18` - Pin definitions for 1.8" TFT Shield V2
======================================================================
"""

from collections import namedtuple
import board

try:
    from micropython import const
except ImportError:

    def const(x):
        return x


from adafruit_seesaw.seesaw import Seesaw

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"

_TIMER_BASE = const(0x08)
_TIMER_PWM = const(0x01)
_TIMER_FREQ = const(0x02)

_TFTSHIELD_RESET_PIN = const(3)

_BUTTON_UP = const(5)
_BUTTON_DOWN = const(8)
_BUTTON_LEFT = const(6)
_BUTTON_RIGHT = const(9)
_BUTTON_SELECT = const(7)
_BUTTON_A = const(10)
_BUTTON_B = const(11)
_BUTTON_C = const(14)

Buttons = namedtuple("Buttons", "right down left up select a b c")


class TFTShield18(Seesaw):

    _BACKLIGHT_ON = b"\xFF\xFF"
    _BACKLIGHT_OFF = b"\x00\x00"

    try:
        _button_mask = (
            (1 << _BUTTON_RIGHT)
            | (1 << _BUTTON_DOWN)
            | (1 << _BUTTON_LEFT)
            | (1 << _BUTTON_UP)
            | (1 << _BUTTON_SELECT)
            | (1 << _BUTTON_A)
            | (1 << _BUTTON_B)
            | (1 << _BUTTON_C)
        )
    except TypeError:
        # During Sphinx build, the following error occurs:
        #  File ".../tftshield18.py", line 60, in TFTShield18
        #    (1 << _BUTTON_B) |
        # TypeError: unsupported operand type(s) for <<: 'int' and '_MockObject'
        _button_mask = 0xFF

    def __init__(self, i2c_bus=board.I2C(), addr=0x2E):
        super(TFTShield18, self).__init__(i2c_bus, addr)
        self.pin_mode(_TFTSHIELD_RESET_PIN, self.OUTPUT)
        self.pin_mode_bulk(self._button_mask, self.INPUT_PULLUP)

    def set_backlight(self, value):
        """
        Set the backlight on
        """
        if not isinstance(value, bool):
            raise ValueError("Value must be of boolean type")
        command = self._BACKLIGHT_ON if value else self._BACKLIGHT_OFF
        self.write(_TIMER_BASE, _TIMER_PWM, b"\x00" + command)

    def set_backlight_freq(self, freq):
        """
        Set the backlight frequency of the TFT Display
        """
        if not isinstance(freq, int):
            raise ValueError("Value must be of integer type")
        value = b"\x00" + bytearray((freq >> 8) & 0xFF, freq & 0xFF)
        self.write(_TIMER_BASE, _TIMER_FREQ, value)

    def tft_reset(self, rst=True):
        """
        Reset the TFT Display
        """
        self.digital_write(_TFTSHIELD_RESET_PIN, rst)

    @property
    def buttons(self):
        """
        Return a set of buttons with current push values
        """
        button_values = self.digital_read_bulk(self._button_mask)
        return Buttons(
            *[
                not button_values & (1 << button)
                for button in (
                    _BUTTON_RIGHT,
                    _BUTTON_DOWN,
                    _BUTTON_LEFT,
                    _BUTTON_UP,
                    _BUTTON_SELECT,
                    _BUTTON_A,
                    _BUTTON_B,
                    _BUTTON_C,
                )
            ]
        )
