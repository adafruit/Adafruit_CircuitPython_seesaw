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
# pylint: disable=missing-docstring,invalid-name,too-many-public-methods,too-few-public-methods

from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"

_CRICKIT_SIGNAL1 = const(2)
_CRICKIT_SIGNAL2 = const(3)
_CRICKIT_SIGNAL3 = const(40)
_CRICKIT_SIGNAL4 = const(41)
_CRICKIT_SIGNAL5 = const(11)
_CRICKIT_SIGNAL6 = const(10)
_CRICKIT_SIGNAL7 = const(9)
_CRICKIT_SIGNAL8 = const(8)

_CRICKIT_SERVO1 = const(17)
_CRICKIT_SERVO2 = const(16)
_CRICKIT_SERVO3 = const(15)
_CRICKIT_SERVO4 = const(14)

_CRICKIT_MOTOR1A = const(22)
_CRICKIT_MOTOR1B = const(23)
_CRICKIT_MOTOR2A = const(19)
_CRICKIT_MOTOR2B = const(18)

_CRICKIT_DRIVE1 = const(13)
_CRICKIT_DRIVE2 = const(12)
_CRICKIT_DRIVE3 = const(43)
_CRICKIT_DRIVE4 = const(42)

_CRICKIT_CAPTOUCH1 = const(4)
_CRICKIT_CAPTOUCH2 = const(5)
_CRICKIT_CAPTOUCH3 = const(6)
_CRICKIT_CAPTOUCH4 = const(7)

class Crickit_Pinmap:
    analog_pins = (_CRICKIT_SIGNAL1, _CRICKIT_SIGNAL2,
                   _CRICKIT_SIGNAL3, _CRICKIT_SIGNAL4,
                   _CRICKIT_SIGNAL5, _CRICKIT_SIGNAL6,
                   _CRICKIT_SIGNAL7, _CRICKIT_SIGNAL8)

    pwm_width = 16

    pwm_pins = (_CRICKIT_SERVO4, _CRICKIT_SERVO3, _CRICKIT_SERVO2, _CRICKIT_SERVO1,
                _CRICKIT_MOTOR1A, _CRICKIT_MOTOR2A,
                _CRICKIT_MOTOR1B, _CRICKIT_MOTOR2B,
                _CRICKIT_DRIVE1, _CRICKIT_DRIVE2,
                _CRICKIT_DRIVE3, _CRICKIT_DRIVE4)

    touch_pins = (_CRICKIT_CAPTOUCH1, _CRICKIT_CAPTOUCH2, _CRICKIT_CAPTOUCH3, _CRICKIT_CAPTOUCH4,
                  _CRICKIT_SIGNAL1, _CRICKIT_SIGNAL2, _CRICKIT_SIGNAL3, _CRICKIT_SIGNAL4)
