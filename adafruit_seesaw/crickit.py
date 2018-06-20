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

_ADC_INPUT_0_PIN_CRICKIT = const(2)
_ADC_INPUT_1_PIN_CRICKIT = const(3)
_ADC_INPUT_2_PIN_CRICKIT = const(40)
_ADC_INPUT_3_PIN_CRICKIT = const(41)
_ADC_INPUT_4_PIN_CRICKIT = const(11)
_ADC_INPUT_5_PIN_CRICKIT = const(10)
_ADC_INPUT_6_PIN_CRICKIT = const(9)
_ADC_INPUT_7_PIN_CRICKIT = const(8)

_CRICKIT_S4 = const(14)
_CRICKIT_S3 = const(15)
_CRICKIT_S2 = const(16)
_CRICKIT_S1 = const(17)

_CRICKIT_M1_A1 = const(18)
_CRICKIT_M1_A2 = const(19)
_CRICKIT_M1_B1 = const(22)
_CRICKIT_M1_B2 = const(23)
_CRICKIT_DRIVE1 = const(42)
_CRICKIT_DRIVE2 = const(43)
_CRICKIT_DRIVE3 = const(12)
_CRICKIT_DRIVE4 = const(13)

_CRICKIT_CT1 = const(4)
_CRICKIT_CT2 = const(5)
_CRICKIT_CT3 = const(6)
_CRICKIT_CT4 = const(7)

class Crickit_Pinmap:
    analog_pins = (_ADC_INPUT_0_PIN_CRICKIT, _ADC_INPUT_1_PIN_CRICKIT,
                   _ADC_INPUT_2_PIN_CRICKIT, _ADC_INPUT_3_PIN_CRICKIT,
                   _ADC_INPUT_4_PIN_CRICKIT, _ADC_INPUT_5_PIN_CRICKIT,
                   _ADC_INPUT_6_PIN_CRICKIT, _ADC_INPUT_7_PIN_CRICKIT)

    pwm_width = 16

    pwm_pins = (_CRICKIT_S4, _CRICKIT_S3, _CRICKIT_S2, _CRICKIT_S1,
                _CRICKIT_M1_A1, _CRICKIT_M1_A2, _CRICKIT_M1_B1,
                _CRICKIT_M1_B2, _CRICKIT_DRIVE1, _CRICKIT_DRIVE2,
                _CRICKIT_DRIVE3, _CRICKIT_DRIVE4)

    touch_pins = (_CRICKIT_CT1, _CRICKIT_CT2, _CRICKIT_CT3, _CRICKIT_CT4)
