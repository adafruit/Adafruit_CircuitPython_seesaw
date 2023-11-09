# SPDX-FileCopyrightText: 2017 Dean Miller for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# pylint: disable=missing-docstring,invalid-name,too-many-public-methods,too-few-public-methods

"""
`adafruit_seesaw.attiny8x7` - Pin definition for Adafruit ATtiny8x7 Breakout with seesaw
==================================================================================
"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"


class ATtiny8x7_Pinmap:
    """This class is automatically used by `adafruit_seesaw.seesaw.Seesaw` when
    a ATtiny8x7 Breakout is detected.

    It is also a reference for the capabilities of each pin."""

    #: The pins capable of analog output
    analog_pins = (0, 1, 2, 3, 6, 7, 18, 19, 20)

    """The effective bit resolution of the PWM pins"""
    pwm_width = 16  # we dont actually use all 16 bits but whatever

    """The pins capable of PWM output"""
    pwm_pins = (0, 1, 9, 12, 13)  # 8 bit PWM mode
    pwm_pins += (6, 7, 8)  # 16 bit PWM mode

    """No pins on this board are capable of touch input"""
    touch_pins = ()
