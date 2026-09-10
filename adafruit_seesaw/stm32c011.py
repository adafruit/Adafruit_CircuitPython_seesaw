# SPDX-FileCopyrightText: 2026 Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Pin capabilities for the experimental STM32C011 seesaw peripheral."""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"


class STM32C011_Pinmap:
    """C011 indices 0..8 are PA0..PA8, 9 is PA11, 10 is PA12, and 15 is PC14.

    Enabled peripheral features may reserve otherwise-capable GPIO pins.
    PWM frequency is shared; PA3/PA11 and PA7/PC14 share timer channels.
    """

    analog_pins = tuple(range(11))
    """Pins supporting the native 12-bit ADC."""

    adc_width = 12
    """Native ADC bit width."""

    pwm_pins = tuple(range(10)) + (15,)
    """PWM-capable pins; PA12 is not PWM-capable."""

    pwm_width = 16
    """Width of the PWM command value."""

    touch_pins = ()
    """No capacitive-touch module is implemented on C011."""
