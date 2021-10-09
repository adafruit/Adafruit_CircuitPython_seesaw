# SPDX-FileCopyrightText: 2017 Dean Miller for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# pylint: disable=missing-docstring,invalid-name,too-many-public-methods,too-few-public-methods

"""
`adafruit_seesaw.attiny8x7` - Pin definition for Adafruit ATtiny8x7 Breakout with seesaw
==================================================================================
"""

try:
    from micropython import const
except ImportError:

    def const(x):
        return x


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"


_PWM_0_PIN = const(0x04)
_PWM_1_PIN = const(0x05)
_PWM_2_PIN = const(0x06)
_PWM_3_PIN = const(0x07)


class ATtiny8x7_Pinmap:
    """This class is automatically used by `adafruit_seesaw.seesaw.Seesaw` when
    a ATtiny8x7 Breakout is detected.

    It is also a reference for the capabilities of each pin."""

    #: The pins capable of analog output
    analog_pins = (0, 1, 2, 3, 6, 7, 18, 19, 20)

    """The effective bit resolution of the PWM pins"""
    pwm_width = 8

    """The pins capable of PWM output"""
    pwm_pins = (_PWM_0_PIN, _PWM_1_PIN, _PWM_2_PIN, _PWM_3_PIN)

    """No pins on this board are capable of touch input"""
    touch_pins = ()
