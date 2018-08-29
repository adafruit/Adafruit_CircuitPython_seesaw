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

from micropython import const
from adafruit_seesaw.seesaw import Seesaw

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"

_KEYPAD_BASE = const(0x10)

_KEYPAD_STATUS = const(0x00)
_KEYPAD_EVENT = const(0x01)
_KEYPAD_INTENSET = const(0x02)
_KEYPAD_INTENCLR = const(0x03)
_KEYPAD_COUNT = const(0x04)
_KEYPAD_FIFO = const(0x10)

# pylint: disable=too-few-public-methods
class KeyEvent:
    def __init__(self, num, edge):
        self.number = int(num)
        self.edge = int(edge)
# pylint: enable=too-few-public-methods

class Keypad(Seesaw):

    EDGE_HIGH = 0
    EDGE_LOW = 1
    EDGE_FALLING = 2
    EDGE_RISING = 3

    def __init__(self, i2c_bus, addr=0x49, drdy=None):
        super(Keypad, self).__init__(i2c_bus, addr, drdy)
        self._interrupt_enabled = False

    @property
    def interrupt_enabled(self):
        return self._interrupt_enabled

    @interrupt_enabled.setter
    def interrupt_enabled(self, value):
        if value not in (True, False):
            raise ValueError("interrupt_enabled must be True or False")

        self._interrupt_enabled = value
        if value:
            self.write8(_KEYPAD_BASE, _KEYPAD_INTENSET, 1)
        else:
            self.write8(_KEYPAD_BASE, _KEYPAD_INTENCLR, 1)

    @property
    def count(self):
        return self.read8(_KEYPAD_BASE, _KEYPAD_COUNT)

    # pylint: disable=unused-argument, no-self-use
    @count.setter
    def count(self, value):
        raise AttributeError("count is read only")
    # pylint: enable=unused-argument, no-self-use

    def set_event(self, key, edge, enable):
        if enable not in (True, False):
            raise ValueError("event enable must be True or False")
        if edge > 3 or edge < 0:
            raise ValueError("invalid edge")

        cmd = bytearray(2)
        cmd[0] = key
        cmd[1] = (1 << (edge+1)) | enable

        self.write(_KEYPAD_BASE, _KEYPAD_EVENT, cmd)

    def read_keypad(self, num):
        ret = bytearray(num)
        self.read(_KEYPAD_BASE, _KEYPAD_FIFO, ret)
        return ret
