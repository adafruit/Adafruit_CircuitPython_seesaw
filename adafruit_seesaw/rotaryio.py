# SPDX-FileCopyrightText: 2017 Dean Miller for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# pylint: disable=missing-docstring,invalid-name,too-many-public-methods


"""
`adafruit_seesaw.digitalio`
====================================================
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"


class IncrementalEncoder:
    """IncrementalEncoder determines the relative rotational position based
    on two series of pulses."""

    def __init__(self, seesaw, encoder=0):
        """Create an IncrementalEncoder object associated with the given
        eesaw device."""
        self._seesaw = seesaw
        self._encoder = encoder

    @property
    def position(self):
        """The current position in terms of pulses. The number of pulses per
        rotation is defined by the specific hardware."""
        return self._seesaw.encoder_position(self._encoder)

    @position.setter
    def position(self, value):
        self._seesaw.set_encoder_position(value, self._encoder)
