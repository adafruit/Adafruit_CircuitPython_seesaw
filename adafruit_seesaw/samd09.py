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

_ADC_INPUT_0_PIN = const(0x02)
_ADC_INPUT_1_PIN = const(0x03)
_ADC_INPUT_2_PIN = const(0x04)
_ADC_INPUT_3_PIN = const(0x05)

_PWM_0_PIN = const(0x04)
_PWM_1_PIN = const(0x05)
_PWM_2_PIN = const(0x06)
_PWM_3_PIN = const(0x07)

class SAMD09_Pinmap:
    analog_pins = (_ADC_INPUT_0_PIN, _ADC_INPUT_1_PIN,
                   _ADC_INPUT_2_PIN, _ADC_INPUT_3_PIN)

    pwm_width = 8

    pwm_pins = (_PWM_0_PIN, _PWM_1_PIN, _PWM_2_PIN, _PWM_3_PIN)

    touch_pins = ()
