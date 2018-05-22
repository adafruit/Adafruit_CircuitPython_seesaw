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

import digitalio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"

class DigitalIO:
    def __init__(self, seesaw, pin):
        self._seesaw = seesaw
        self._pin = pin
        self._drive_mode = digitalio.DriveMode.PUSH_PULL
        self._direction = False
        self._pull = None
        self._value = False

    def deinit(self):
        pass

    def switch_to_output(self, value=False, drive_mode=digitalio.DriveMode.PUSH_PULL):
        self._seesaw.pin_mode(self._pin, self._seesaw.OUTPUT)
        self._seesaw.digital_write(self._pin, value)
        self._drive_mode = drive_mode
        self._pull = None

    def switch_to_input(self, pull=None):
        if pull == digitalio.Pull.DOWN:
            raise ValueError("Pull Down currently not supported")
        elif pull == digitalio.Pull.UP:
            self._seesaw.pin_mode(self._pin, self._seesaw.INPUT_PULLUP)
        else:
            self._seesaw.pin_mode(self._pin, self._seesaw.INPUT)
        self._pull = pull

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value == digitalio.Direction.OUTPUT:
            self.switch_to_output()
        elif value == digitalio.Direction.INPUT:
            self.switch_to_input()
        else:
            raise ValueError("Out of range")
        self._direction = value

    @property
    def value(self):
        if self._direction == digitalio.Direction.OUTPUT:
            return self._value
        return self._seesaw.digital_read(self._pin)

    @value.setter
    def value(self, val):
        if not 0 <= val <= 1:
            raise ValueError("Out of range")
        self._seesaw.digital_write(self._pin, val)
        self._value = val

    @property
    def drive_mode(self):
        return self._drive_mode

    @drive_mode.setter
    def drive_mode(self, mode):
        pass

    @property
    def pull(self):
        return self._pull

    @pull.setter
    def pull(self, mode):
        if self._direction == digitalio.Direction.OUTPUT:
            raise AttributeError("cannot set pull on an output pin")
        elif mode == digitalio.Pull.DOWN:
            raise ValueError("Pull Down currently not supported")
        elif mode == digitalio.Pull.UP:
            self._seesaw.pin_mode(self._pin, self._seesaw.INPUT_PULLUP)
        elif mode is None:
            self._seesaw.pin_mode(self._pin, self._seesaw.INPUT)
        else:
            raise ValueError("Out of range")
