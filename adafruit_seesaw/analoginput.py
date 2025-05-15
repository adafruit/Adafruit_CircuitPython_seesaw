# SPDX-FileCopyrightText: 2017 Dean Miller for Adafruit Industries
#
# SPDX-License-Identifier: MIT


"""
`adafruit_seesaw.analoginput`
====================================================
"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"


class AnalogInput:
    """CircuitPython-compatible class for analog inputs

    This class is intended to be a compatible subset of `analogio.AnalogIn`

    :param ~adafruit_seesaw.seesaw.Seesaw seesaw: The device
    :param int pin: The pin number on the device"""

    def __init__(self, seesaw, pin, delay=0.008):
        self._seesaw = seesaw
        self._pin = pin
        self._delay = delay

    def deinit(self):
        pass

    @property
    def value(self):
        """The current analog value on the pin, as an integer from 0..65535 (inclusive)"""
        return self._seesaw.analog_read(self._pin, self._delay)

    @property
    def reference_voltage(self):
        """The reference voltage for the pin"""
        return 3.3
