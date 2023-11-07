# SPDX-FileCopyrightText: 2017 Dean Miller for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# pylint: disable=missing-docstring,invalid-name,too-many-public-methods,too-few-public-methods
"""
`adafruit_seesaw.attinyx16` - Pin definition for Adafruit ATtinyx16 Breakout with seesaw
==================================================================================
"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"


class ATtinyx16_Pinmap:
    """This class is automatically used by `adafruit_seesaw.seesaw.Seesaw` when
    a ATtinyx16 Breakout (PID 5690, PID 5681) is detected.

    It is also a reference for the capabilities of each pin."""

    """The pins capable of analog output"""
    analog_pins = (0, 1, 2, 3, 4, 5, 14, 15, 16)

    """The effective bit resolution of the PWM pins"""
    pwm_width = 16  # we dont actually use all 16 bits but whatever

    """The pins capable of PWM output"""
    pwm_pins = (0, 1, 7, 11, 16)  # 8 bit PWM mode
    pwm_pins += (4, 5, 6)  # 16 bit PWM mode

    """No pins on this board are capable of touch input"""
    touch_pins = ()
