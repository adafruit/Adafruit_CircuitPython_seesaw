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
"""
`adafruit_seesaw`
====================================================

An I2C to whatever helper chip.

* Author(s): Dean Miller

Implementation Notes
--------------------

**Hardware:**

* Adafruit `ATSAMD09 Breakout with seesaw
  <https://www.adafruit.com/product/3657>`_ (Product ID: 3657)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the ESP8622 and M0-based boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# This code needs to be broken up into analogio, busio, digitalio, and pulseio
# compatible classes so we won't bother with some lints until then.
# pylint: disable=missing-docstring,invalid-name,too-many-public-methods

import time

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
import digitalio
import struct

_STATUS_BASE = const(0x00)
_GPIO_BASE = const(0x01)
_SERCOM0_BASE = const(0x02)

_TIMER_BASE = const(0x08)
_ADC_BASE = const(0x09)
_DAC_BASE = const(0x0A)
_INTERRUPT_BASE = const(0x0B)
_DAP_BASE = const(0x0C)
_EEPROM_BASE = const(0x0D)
_NEOPIXEL_BASE = const(0x0E)
_TOUCH_BASE = const(0x0F)

_GPIO_DIRSET_BULK = const(0x02)
_GPIO_DIRCLR_BULK = const(0x03)
_GPIO_BULK = const(0x04)
_GPIO_BULK_SET = const(0x05)
_GPIO_BULK_CLR = const(0x06)
_GPIO_BULK_TOGGLE = const(0x07)
_GPIO_INTENSET = const(0x08)
_GPIO_INTENCLR = const(0x09)
_GPIO_INTFLAG = const(0x0A)
_GPIO_PULLENSET = const(0x0B)
_GPIO_PULLENCLR = const(0x0C)

_STATUS_HW_ID = const(0x01)
_STATUS_VERSION = const(0x02)
_STATUS_OPTIONS = const(0x03)
_STATUS_SWRST = const(0x7F)

_TIMER_STATUS = const(0x00)
_TIMER_PWM = const(0x01)
_TIMER_FREQ = const(0x02)

_ADC_STATUS = const(0x00)
_ADC_INTEN = const(0x02)
_ADC_INTENCLR = const(0x03)
_ADC_WINMODE = const(0x04)
_ADC_WINTHRESH = const(0x05)
_ADC_CHANNEL_OFFSET = const(0x07)

_SERCOM_STATUS = const(0x00)
_SERCOM_INTEN = const(0x02)
_SERCOM_INTENCLR = const(0x03)
_SERCOM_BAUD = const(0x04)
_SERCOM_DATA = const(0x05)

_NEOPIXEL_STATUS = const(0x00)
_NEOPIXEL_PIN = const(0x01)
_NEOPIXEL_SPEED = const(0x02)
_NEOPIXEL_BUF_LENGTH = const(0x03)
_NEOPIXEL_BUF = const(0x04)
_NEOPIXEL_SHOW = const(0x05)

_TOUCH_CHANNEL_OFFSET = const(0x10)

_ADC_INPUT_0_PIN = const(0x02)
_ADC_INPUT_1_PIN = const(0x03)
_ADC_INPUT_2_PIN = const(0x04)
_ADC_INPUT_3_PIN = const(0x05)

_ADC_INPUT_0_PIN_CRCKIT = const(2)
_ADC_INPUT_1_PIN_CRCKIT = const(3)
_ADC_INPUT_2_PIN_CRCKIT = const(40)
_ADC_INPUT_3_PIN_CRCKIT = const(41)
_ADC_INPUT_4_PIN_CRCKIT = const(11)
_ADC_INPUT_5_PIN_CRCKIT = const(10)
_ADC_INPUT_6_PIN_CRCKIT = const(9)
_ADC_INPUT_7_PIN_CRCKIT = const(8)

_PWM_0_PIN = const(0x04)
_PWM_1_PIN = const(0x05)
_PWM_2_PIN = const(0x06)
_PWM_3_PIN = const(0x07)

_CRCKIT_S4 = const(14)
_CRCKIT_S3 = const(15)
_CRCKIT_S2 = const(16)
_CRCKIT_S1 = const(17)

_CRCKIT_M1_A1 = const(18)
_CRCKIT_M1_A2 = const(19)
_CRCKIT_M1_B1 = const(22)
_CRCKIT_M1_B2 = const(23)
_CRCKIT_DRIVE1 = const(42)
_CRCKIT_DRIVE2 = const(43)
_CRCKIT_DRIVE3 = const(12)
_CRCKIT_DRIVE4 = const(13)

_CRCKIT_CT1 = const(0)
_CRCKIT_CT2 = const(1)
_CRCKIT_CT3 = const(2)
_CRCKIT_CT4 = const(3)

_HW_ID_CODE = const(0x55)
_EEPROM_I2C_ADDR = const(0x3F)

SEESAW_SAMD09 = const(0x00)
SEESAW_CRCKIT = const(0x01)

#TODO: update when we get real PID
_CRCKIT_PID = const(9999)

class DigitalIO:
    def __init__(self, seesaw, pin):
        self._seesaw = seesaw
        self._pin = pin
        self._drive_mode = digitalio.DriveMode.PUSH_PULL
        self._direction = False
        self._pull = None
        self._value = False

    def deinit(self):
        pass

    def switch_to_output(self, value=False, drive_mode=digitalio.DriveMode.PUSH_PULL):
        self._seesaw.pin_mode(self._pin, self._seesaw.OUTPUT)
        self._seesaw.digital_write(self._pin, value)
        self._drive_mode = drive_mode
        self._pull = None

    def switch_to_input(self, pull=None):
        if pull == digitalio.Pull.DOWN:
            raise ValueError("Pull Down currently not supported")
        elif pull == digitalio.Pull.UP:
            self._seesaw.pin_mode(self._pin, self._seesaw.INPUT_PULLUP)
        else:
            self._seesaw.pin_mode(self._pin, self._seesaw.INPUT)
        self._pull = pull

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value == digitalio.Direction.OUTPUT:
            self.switch_to_output()
        elif value == digitalio.Direction.INPUT:
            self.switch_to_input()
        else:
            raise ValueError("Out of range")
        self._direction = value

    @property
    def value(self):
        if self._direction == digitalio.Direction.OUTPUT:
            return self._value
        else:
            return self._seesaw.digital_read(self._pin)

    @value.setter
    def value(self, val):
        if not 0 <= val <= 1:
            raise ValueError("Out of range")
        self._seesaw.digital_write(self._pin, val)
        self._value = val

    @property
    def drive_mode(self):
        return self._drive_mode

    @drive_mode.setter
    def drive_mode(self, mode):
        pass

    @property
    def pull(self):
        return self._pull

    @pull.setter
    def pull(self, mode):
        if self._direction == digitalio.Direction.OUTPUT:
            raise AttributeError("cannot set pull on an output pin")
        elif mode == digitalio.Pull.DOWN:
            raise ValueError("Pull Down currently not supported")
        elif mode == digitalio.Pull.UP:
            self._seesaw.pin_mode(self._pin, self._seesaw.INPUT_PULLUP)
        elif mode == None:
            self._seesaw.pin_mode(self._pin, self._seesaw.INPUT)
        else:
            raise ValueError("Out of range")

class AnalogInput:
    def __init__(self, seesaw, pin):
        self._seesaw = seesaw
        self._pin = pin

    def deinit(self):
        pass

    @property
    def value(self):
        return self._seesaw.analog_read(self._pin)

    @property
    def reference_voltage(self):
        return 3.3

class PWMChannel:
    """A single seesaw channel that matches the :py:class:`~pulseio.PWMOut` API."""
    def __init__(self, seesaw, pin):
        self._seesaw = seesaw
        self._pin = pin
        self._dc = 0
        self._frequency = 0

    @property
    def frequency(self):
        """The overall PWM frequency in herz."""
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        self._seesaw.set_pwm_freq(self._pin, frequency)
        self._frequency = frequency

    @property
    def duty_cycle(self):
        """16 bit value that dictates how much of one cycle is high (1) versus low (0). 0xffff will
           always be high, 0 will always be low and 0x7fff will be half high and then half low."""
        return self._dc

    @duty_cycle.setter
    def duty_cycle(self, value):
        if not 0 <= value <= 0xffff:
            raise ValueError("Out of range")
        self._seesaw.analog_write(self._pin, value)
        self._dc = value

class SeesawNeopixel:
    def __init__(self, seesaw, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):
        self._seesaw = seesaw
        self._pin = pin
        self._bpp = bpp
        self._auto_write = auto_write
        self._pixel_order = pixel_order
        self._n = n

        cmd = bytearray([pin])
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_PIN, cmd)
        cmd = struct.pack(">H", n*self._bpp)
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF_LENGTH, cmd)

    @property
    def brightness(self):
        pass

    @brightness.setter
    def brightness(self, value):
        pass

    def deinit(self):
        pass

    def __len__(self):
        return self._n

    def __setitem__(self, key, value):
        cmd = bytearray(6)
        cmd[:2] = struct.pack(">H", key * self._bpp)
        cmd[2:] = struct.pack(">I", value)
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF, cmd)
        if self._auto_write:
            self.show()

    def __getitem__(self, key):
        pass

    def fill(self, color):
        cmd = bytearray(self._n*self._bpp+2)
        for i in range(self._n):
            cmd[self._bpp*i+2:] = struct.pack(">I", color)

        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_BUF, cmd)

        if self._auto_write:
            self.show()

    def show(self):
        self._seesaw.write(_NEOPIXEL_BASE, _NEOPIXEL_SHOW)

class Seesaw:
    """Driver for Seesaw i2c generic conversion trip

       :param ~busio.I2C i2c_bus: Bus the SeeSaw is connected to
       :param int addr: I2C address of the SeeSaw device"""
    INPUT = const(0x00)
    OUTPUT = const(0x01)
    INPUT_PULLUP = const(0x02)

    def __init__(self, i2c_bus, addr=0x49, drdy=None):
        self._drdy = drdy
        if drdy != None:
            drdy.switch_to_input()

        self.i2c_device = I2CDevice(i2c_bus, addr)
        self.sw_reset()

    def sw_reset(self):
        """Trigger a software reset of the SeeSaw chip"""
        self.write8(_STATUS_BASE, _STATUS_SWRST, 0xFF)
        time.sleep(.500)

        chip_id = self.read8(_STATUS_BASE, _STATUS_HW_ID)

        if chip_id != _HW_ID_CODE:
            raise RuntimeError("Seesaw hardware ID returned (0x{:x}) is not "
                               "correct! Expected 0x{:x}. Please check your wiring."
                               .format(chip_id, _HW_ID_CODE))

        pid = self.get_version() >> 16
        if pid == _CRCKIT_PID:
            self.variant = SEESAW_CRCKIT
        else:
            self.variant = SEESAW_SAMD09

    def get_options(self):
        buf = bytearray(4)
        self.read(_STATUS_BASE, _STATUS_OPTIONS, buf, 4)
        ret = struct.unpack(">I", buf)[0]
        return ret

    def get_version(self):
        buf = bytearray(4)
        self.read(_STATUS_BASE, _STATUS_VERSION, buf, 4)
        ret = struct.unpack(">I", buf)[0]
        return ret

    def get_digitalio(self, pin):
        return DigitalIO(self, pin)

    def pin_mode(self, pin, mode):
        if pin >= 32:
            self.pin_mode_bulk_b(1 << (pin - 32), mode)
        else:
            self.pin_mode_bulk(1 << pin, mode)

    def digital_write(self, pin, value):
        if pin >= 32:
            self.digital_write_bulk_b(1 << (pin - 32), value)
        else:
            self.digital_write_bulk(1 << pin, value)

    def digital_read(self, pin):
        if pin >= 32:
            return self.digital_read_bulk_b((1 << (pin - 32))) != 0
        else:
            return self.digital_read_bulk((1 << pin)) != 0

    def digital_read_bulk(self, pins):
        buf = bytearray(4)
        self.read(_GPIO_BASE, _GPIO_BULK, buf)
        ret = struct.unpack(">I", buf)[0]
        return ret & pins

    def digital_read_bulk_b(self, pins):
        buf = bytearray(8)
        self.read(_GPIO_BASE, _GPIO_BULK, buf)
        ret = struct.unpack(">II", buf)[1]
        return ret & pins


    def set_GPIO_interrupts(self, pins, enabled):
        cmd = struct.pack(">I", pins)
        if enabled:
            self.write(_GPIO_BASE, _GPIO_INTENSET, cmd)
        else:
            self.write(_GPIO_BASE, _GPIO_INTENCLR, cmd)

    def get_neopixel(self, pin, n, bpp=3, brightness=1.0, auto_write=True, 
                     pixel_order=None):
        return SeesawNeopixel(self, pin, n, bpp=bpp, brightness=brightness, 
                              auto_write=auto_write, pixel_order=pixel_order)

    def get_analog_in(self, pin):
        return AnalogInput(self, pin)

    def analog_read(self, pin):
        buf = bytearray(2)
        if self.variant == SEESAW_CRCKIT:
            pin_mapping = [_ADC_INPUT_0_PIN_CRCKIT, _ADC_INPUT_1_PIN_CRCKIT,
                           _ADC_INPUT_2_PIN_CRCKIT, _ADC_INPUT_3_PIN_CRCKIT,
                           _ADC_INPUT_4_PIN_CRCKIT, _ADC_INPUT_5_PIN_CRCKIT,
                           _ADC_INPUT_6_PIN_CRCKIT, _ADC_INPUT_7_PIN_CRCKIT]
        else:
            pin_mapping = [_ADC_INPUT_0_PIN, _ADC_INPUT_1_PIN,
                           _ADC_INPUT_2_PIN, _ADC_INPUT_3_PIN]

        if pin not in pin_mapping:
            raise ValueError("Invalid ADC pin")

        self.read(_ADC_BASE, _ADC_CHANNEL_OFFSET + pin_mapping.index(pin), buf)
        ret = struct.unpack(">H", buf)[0]
        time.sleep(.001)
        return ret

    def touch_read(self, pin):
        buf = bytearray(2)

        pin_mapping = [_CRCKIT_CT1, _CRCKIT_CT2, _CRCKIT_CT3, _CRCKIT_CT4]

        if pin not in pin_mapping:
            raise ValueError("Invalid touch pin")

        self.read(_TOUCH_BASE, _TOUCH_CHANNEL_OFFSET + pin_mapping.index(pin), buf)
        ret = struct.unpack(">H", buf)[0]
        return ret

    def pin_mode_bulk(self, pins, mode):
        cmd = struct.pack(">I", pins)
        if mode == self.OUTPUT:
            self.write(_GPIO_BASE, _GPIO_DIRSET_BULK, cmd)
        elif mode == self.INPUT:
            self.write(_GPIO_BASE, _GPIO_DIRCLR_BULK, cmd)

        elif mode == self.INPUT_PULLUP:
            self.write(_GPIO_BASE, _GPIO_DIRCLR_BULK, cmd)
            self.write(_GPIO_BASE, _GPIO_PULLENSET, cmd)
            self.write(_GPIO_BASE, _GPIO_BULK_SET, cmd)

    def pin_mode_bulk_b(self, pins, mode):
        cmd = bytearray(8)
        cmd[4:] = struct.pack(">I", pins)
        if mode == self.OUTPUT:
            self.write(_GPIO_BASE, _GPIO_DIRSET_BULK, cmd)
        elif mode == self.INPUT:
            self.write(_GPIO_BASE, _GPIO_DIRCLR_BULK, cmd)

        elif mode == self.INPUT_PULLUP:
            self.write(_GPIO_BASE, _GPIO_DIRCLR_BULK, cmd)
            self.write(_GPIO_BASE, _GPIO_PULLENSET, cmd)
            self.write(_GPIO_BASE, _GPIO_BULK_SET, cmd)

    def digital_write_bulk(self, pins, value):
        cmd = struct.pack(">I", pins)
        if value:
            self.write(_GPIO_BASE, _GPIO_BULK_SET, cmd)
        else:
            self.write(_GPIO_BASE, _GPIO_BULK_CLR, cmd)


    def digital_write_bulk_b(self, pins, value):
        cmd = bytearray(8)
        cmd[4:] = struct.pack(">I", pins)
        if value:
            self.write(_GPIO_BASE, _GPIO_BULK_SET, cmd)
        else:
            self.write(_GPIO_BASE, _GPIO_BULK_CLR, cmd)

    def get_pwm(self, pin):
        return PWMChannel(self, pin)

    def analog_write(self, pin, value):
        if self.variant == SEESAW_CRCKIT:
            pin_mapping = [_CRCKIT_S4, _CRCKIT_S3, _CRCKIT_S2, _CRCKIT_S1,
                           _CRCKIT_M1_A1, _CRCKIT_M1_A2, _CRCKIT_M1_B1,
                           _CRCKIT_M1_B2, _CRCKIT_DRIVE1, _CRCKIT_DRIVE2,
                           _CRCKIT_DRIVE3, _CRCKIT_DRIVE4]
            if pin in pin_mapping:
                cmd = bytearray([pin_mapping.index(pin), (value >> 8), value])
                self.write(_TIMER_BASE, _TIMER_PWM, cmd)
        else:
            pin_mapping = [_PWM_0_PIN, _PWM_1_PIN, _PWM_2_PIN, _PWM_3_PIN]
            if pin in pin_mapping:
                cmd = bytearray([pin_mapping.index(pin), value])
                self.write(_TIMER_BASE, _TIMER_PWM, cmd)

    def set_pwm_freq(self, pin, freq):
        if self.variant == SEESAW_CRCKIT:
            pin_mapping = [_CRCKIT_S4, _CRCKIT_S3, _CRCKIT_S2, _CRCKIT_S1,
                           _CRCKIT_M1_A1, _CRCKIT_M1_A2, _CRCKIT_M1_B1,
                           _CRCKIT_M1_B2, _CRCKIT_DRIVE1, _CRCKIT_DRIVE2,
                           _CRCKIT_DRIVE3, _CRCKIT_DRIVE4]
        else:
            pin_mapping = [_PWM_0_PIN, _PWM_1_PIN, _PWM_2_PIN, _PWM_3_PIN]

        if pin in pin_mapping:
            cmd = bytearray([pin_mapping.index(pin), (freq >> 8), freq])
            self.write(_TIMER_BASE, _TIMER_FREQ, cmd)

    # def enable_sercom_data_rdy_interrupt(self, sercom):
    #
    #     _sercom_inten.DATA_RDY = 1
    #     self.write8(SEESAW_SERCOM0_BASE + sercom, SEESAW_SERCOM_INTEN, _sercom_inten.get())
    #
    #
    # def disable_sercom_data_rdy_interrupt(self, sercom):
    #
    #     _sercom_inten.DATA_RDY = 0
    #     self.write8(SEESAW_SERCOM0_BASE + sercom, SEESAW_SERCOM_INTEN, _sercom_inten.get())
    #
    #
    # def read_sercom_data(self, sercom):
    #
    #     return self.read8(SEESAW_SERCOM0_BASE + sercom, SEESAW_SERCOM_DATA)

    def set_i2c_addr(self, addr):
        self.eeprom_write8(_EEPROM_I2C_ADDR, addr)
        time.sleep(.250)
        self.i2c_device.device_address = addr
        self.sw_reset()

    def get_i2c_addr(self):
        return self.read8(_EEPROM_BASE, _EEPROM_I2C_ADDR)

    def eeprom_write8(self, addr, val):
        self.eeprom_write(addr, bytearray([val]))

    def eeprom_write(self, addr, buf):
        self.write(_EEPROM_BASE, addr, buf)

    def eeprom_read8(self, addr):
        return self.read8(_EEPROM_BASE, addr)

    def uart_set_baud(self, baud):
        cmd = struct.pack(">I", baud)
        self.write(_SERCOM0_BASE, _SERCOM_BAUD, cmd)

    def write8(self, reg_base, reg, value):
        self.write(reg_base, reg, bytearray([value]))

    def read8(self, reg_base, reg):
        ret = bytearray(1)
        self.read(reg_base, reg, ret)
        return ret[0]

    def read(self, reg_base, reg, buf, delay=.001):
        self.write(reg_base, reg)
        if self._drdy != None:
            while self._drdy.value == False:
                pass
        else:
            time.sleep(delay)
        with self.i2c_device as i2c:
            i2c.readinto(buf)

    def write(self, reg_base, reg, buf=None):
        full_buffer = bytearray([reg_base, reg])
        if buf is not None:
            full_buffer += buf

        if self._drdy != None:
            while self._drdy.value == False:
                pass
        with self.i2c_device as i2c:
            i2c.write(full_buffer)
