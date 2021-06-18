# SPDX-FileCopyrightText: 2021 Greg Paris for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# pylint: disable=missing-docstring,invalid-name,too-many-public-methods

"""
`adafruit_seesaw.neokey_1x4`
====================================================

Four Mechanical Key Switches with NeoPixels - STEMMA/QT/Qwiic

* Author(s): Greg Paris with credit to Dean Miller

Implementation Notes
--------------------

**Hardware:**

* Adafruit `NeoKey 1x4 QT I2C
  <https://www.adafruit.com/product/4980>` _ (Product ID: 4980)

**Software and Dependencies:**

* Adafruit CircuitPython firmware: https://circuitpython.org/
* or Adafruit Blinka: https://circuitpython.org/blinka
* Adafruit's Bus Device Library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

try:
    from micropython import const
except ImportError:

    def const(x):
        return x


from collections import namedtuple
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.neopixel import NeoPixel, GRB

_NK14_ADDR = const(0x30)
_NK14_NEOPIXEL = const(3)
_NK14_KEY0 = const(1 << 4)
_NK14_KEY1 = const(1 << 5)
_NK14_KEY2 = const(1 << 6)
_NK14_KEY3 = const(1 << 7)
_NK14_KEYMASK = const(_NK14_KEY0 | _NK14_KEY1 | _NK14_KEY2 | _NK14_KEY3)
_NK14_KEYS = (_NK14_KEY0, _NK14_KEY1, _NK14_KEY2, _NK14_KEY3)
_NK14_COUNT = const(4)

# Event class used for both single- and multi-NeoKey_1x4
_KeyEvent = namedtuple("_KeyEvent", "obj key action".split())

def _bits_to_keys(bits):
    return [k for k in range(_NK14_COUNT) if _NK14_KEYS[k] & bits]

class NeoKey_1x4(Seesaw):
    """Implements the Seesaw-based four-key I2C keyboard with Neopixel lights

    :param ~busio.I2C i2c_bus: Bus the NeoKey_1x4 is connected to
    :param int addr: I2C address of the NeoKey_1x4 device
    :param ~digitalio.DigitalInOut drdy: Pin connected to NeoKey_1x4's 'ready' output
    :param float brightness: NeoPixel intensity
    :param ~auto_write: NeoPixel auto-show"""


    #: Indicates that the key was recently released
    RELEASED = 0
    #: Indicates that the key was recently pressed
    PRESSED = 1

    def __init__(self, i2c_bus, addr=_NK14_ADDR, *, brightness=1.0, auto_write=True):
        super().__init__(i2c_bus, addr, None) # drdy omitted from our __init__
        self._pixels = NeoPixel(
            self, # we're a child of Seesaw
            _NK14_NEOPIXEL,
            _NK14_COUNT,
            pixel_order=GRB,
            brightness=brightness,
            auto_write=auto_write,
        )
        self._pixels.fill(0)
        self._callback = [None] * _NK14_COUNT
        self._pressed = 0
        self.pin_mode_bulk(_NK14_KEYMASK, self.INPUT_PULLUP)
        # don't know the purpose of interrupts, but Arduino code does this
        self.set_GPIO_interrupts(_NK14_KEYMASK, True)

    def __getitem__(self, key):
        return self._pixels[key]

    def __setitem__(self, key, color):
        self._pixels[key] = color

    def __iter__(self):
        return (key for key in range(_NK14_COUNT))

    def __len__(self):
        return _NK14_COUNT

    def fill(self, color):
        self._pixels.fill(color)

    def show(self):
        self._pixels.show()

    @property
    def auto_write(self):
        return self._pixels.auto_write

    @auto_write.setter
    def auto_write(self, value):
        self._pixels.auto_write = value

    @property
    def brightness(self):
        return self._pixels.brightness

    @brightness.setter
    def brightness(self, value):
        self._pixels.brightness = value

    def read_keys(self):
        """Read key status from the NeoKey_1x4
            Invoke callbacks if any keys have just been pressed or released
            Return lists of keys currently pressed, just pressed and just released"""
        # next several lifted from Adafruit_NeoKey_1x4.cpp
        pressed = self.digital_read_bulk(_NK14_KEYMASK)
        pressed ^= _NK14_KEYMASK # invert
        pressed &= _NK14_KEYMASK # re-mask
        just_pressed = (pressed ^ self._pressed) & pressed
        just_released = (pressed ^ self._pressed) & ~pressed
        self._pressed = pressed
        keys_pressed = _bits_to_keys(pressed)
        keys_just_pressed = _bits_to_keys(just_pressed)
        keys_just_released = _bits_to_keys(just_released)
        for key in keys_just_pressed:
            if self._callback[key]:
                self._callback[key](_KeyEvent(self, key, self.PRESSED))
        for key in keys_just_released:
            if self._callback[key]:
                self._callback[key](_KeyEvent(self, key, self.RELEASED))
        return keys_pressed, keys_just_pressed, keys_just_released

    def register_callback(self, key, function):
        """Register a callback to be run when key is pressed/released"""
        self._callback[key] = function

    def deregister_callback(self, key):
        self._callback[key] = None

def _localize(xy):
    """Board coords and key number from x,y coords"""
    x, y = xy
    return ((x // _NK14_COUNT, y), x % _NK14_COUNT)

def _globalize(xy, key):
    """Coordinates from board x,y and key number"""
    x, y = xy
    return (x * _NK14_COUNT + key, y)

class MultiNeoKey_1x4():
    """Implements a two-dimensional arrangement of NeoKey_1x4's

    :param ~busio.I2C i2c_bus: Bus the NeoKey_1x4 is connected to
    :param list[list[int]] addrs: list[col][row] of I2C addresses of the NeoKey_1x4 devices
    :param float brightness: NeoPixel intensity
    :param ~auto_write: NeoPixel auto-show"""

    def __init__(self, i2c_bus, addrs, *, brightness=1.0, auto_write=True):
        # doesn't need to be rectangular or contiguous, but must be 2D
        self._brightness = brightness
        self._auto_write = auto_write
        self._nk14 = {}
        self._callback = {}
        for y, row in enumerate(addrs):
            for x, i2c_addr in enumerate(row):
                if i2c_addr is not None: # allow gaps
                    self._nk14[x, y] = NeoKey_1x4(
                        i2c_bus,
                        i2c_addr,
                        brightness=brightness,
                        auto_write=auto_write,
                    )

    def __getitem__(self, xy):
        xy, key = _localize(xy)
        return self._nk14[xy][key]

    def __setitem__(self, xy, color):
        xy, key = _localize(xy)
        self._nk14[xy][key] = color

    def __iter__(self):
        return (key for key in self._nk14)

    def __len__(self):
        return len(self._nk14) * _NK14_COUNT

    def read_keys(self):
        """Read key status from all NeoKey_1x4 keys
            Invoke callbacks if any keys have just been pressed or released
            Return lists of keys currently pressed, just pressed and just released"""
        pressed = []
        just_pressed = []
        just_released = []
        for xy, nk in self._nk14.items():
            pr, jpr, jrel = nk.read_keys()
            pressed.extend([_globalize(xy, key) for key in pr])
            just_pressed.extend([_globalize(xy, key) for key in jpr])
            just_released.extend([_globalize(xy, key) for key in jrel])
        for xy in just_pressed:
            if xy in self._callback:
                self._callback[xy](_KeyEvent(self, xy, NeoKey_1x4.PRESSED))
        for xy in just_released:
            if xy in self._callback:
                self._callback[xy](_KeyEvent(self, xy, NeoKey_1x4.RELEASED))
        return pressed, just_pressed, just_released

    def register_callback(self, xy, function):
        # We don't use the individual NeoKey_1x4 callbacks because the
        # callback function would not necessarily expect an integer key
        # instead of x, y. So we use a separate set of callbacks.
        bxy, key = _localize(xy)
        if bxy not in self._nk14 or key < 0 or key >= _NK14_COUNT:
            raise KeyError(f"No NeoKey_1x4 key at {xy}")
        if function is not None:
            self._callback[xy] = function
        else:
            try:
                del self._callback[xy]
            except KeyError:
                pass # deregistering nothing is okay

    def deregister_callback(self, xy):
        self.register_callback(xy, None)

    def fill(self, color):
        for nk in self._nk14.values():
            nk.fill(color)

    def show(self):
        for nk in self._nk14.values():
            nk.show()

    @property
    def auto_write(self):
        return self._auto_write

    @auto_write.setter
    def auto_write(self, value):
        if self._auto_write != value:
            self._auto_write = value
            for nk in self._nk14.values():
                nk.auto_write = value

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        if self._brightness != value:
            self._brightness = value
            for nk in self._nk14.values():
                nk.brightness = value
