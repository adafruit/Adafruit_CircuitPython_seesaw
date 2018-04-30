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

class Seesaw:
    """Driver for Seesaw i2c generic conversion trip

       :param ~busio.I2C i2c_bus: Bus the SeeSaw is connected to
       :param int addr: I2C address of the SeeSaw device"""
    INPUT = const(0x00)
    OUTPUT = const(0x01)
    INPUT_PULLUP = const(0x02)

    def __init__(self, i2c_bus, addr=0x49):
        self.i2c_device = I2CDevice(i2c_bus, addr)
        self.sw_reset()

    def sw_reset(self):
        """Trigger a software reset of the SeeSaw chip"""
        self.write8(_STATUS_BASE, _STATUS_SWRST, 0xFF)
        time.sleep(.500)

        chip_id = self.read8(_STATUS_BASE, _STATUS_HW_ID)

        if chip_id != _HW_ID_CODE:
            raise RuntimeError("Seesaw hardware ID returned ({:x}) is not "
                               "correct! Expected {:x}. Please check your wiring."
                               .format(chip_id, _HW_ID_CODE))

        pid = self.get_version() >> 16
        if(pid == _CRCKIT_PID):
            self.variant = SEESAW_CRCKIT
        else:
            self.variant = SEESAW_SAMD09

    def get_options(self):
        buf = bytearray(4)
        self.read(_STATUS_BASE, _STATUS_OPTIONS, buf, 4)
        ret = (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3]
        return ret

    def get_version(self):
        buf = bytearray(4)
        self.read(_STATUS_BASE, _STATUS_VERSION, buf, 4)
        ret = (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3]
        return ret

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
        return self.digital_read_bulk((1 << pin)) != 0

    def digital_read_bulk(self, pins):
        buf = bytearray(4)
        self.read(_GPIO_BASE, _GPIO_BULK, buf)
        #TODO: weird overflow error, fix
        ret = ((buf[0] & 0xF) << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3]
        return ret & pins

    def set_GPIO_interrupts(self, pins, enabled):
        cmd = bytearray([(pins >> 24), (pins >> 16), (pins >> 8), pins])
        if enabled:
            self.write(_GPIO_BASE, _GPIO_INTENSET, cmd)
        else:
            self.write(_GPIO_BASE, _GPIO_INTENCLR, cmd)

    def analog_read(self, pin):
        buf = bytearray(2)
        if self.variant == SEESAW_CRCKIT:
            pin_mapping = [_ADC_INPUT_0_PIN_CRCKIT, _ADC_INPUT_1_PIN_CRCKIT, _ADC_INPUT_2_PIN_CRCKIT,
                _ADC_INPUT_3_PIN_CRCKIT, _ADC_INPUT_4_PIN_CRCKIT, _ADC_INPUT_5_PIN_CRCKIT,
                _ADC_INPUT_6_PIN_CRCKIT, _ADC_INPUT_7_PIN_CRCKIT]
        else:
            pin_mapping = [_ADC_INPUT_0_PIN, _ADC_INPUT_1_PIN,
                       _ADC_INPUT_2_PIN, _ADC_INPUT_3_PIN]

        if pin not in pin_mapping:
            raise ValueError("Invalid ADC pin")

        self.read(_ADC_BASE, _ADC_CHANNEL_OFFSET + pin_mapping.index(pin), buf)
        ret = (buf[0] << 8) | buf[1]
        time.sleep(.001)
        return ret

    def touch_read(self, pin):
        buf = bytearray(2)

        pin_mapping = [_CRCKIT_CT1, _CRCKIT_CT2, _CRCKIT_CT3, _CRCKIT_CT4]

        if pin not in pin_mapping:
            raise ValueError("Invalid touch pin")

        self.read(_TOUCH_BASE, _TOUCH_CHANNEL_OFFSET + pin_mapping.index(pin), buf)
        ret = (buf[0] << 8) | buf[1]
        return ret

    def pin_mode_bulk(self, pins, mode):
        cmd = bytearray([(pins >> 24), (pins >> 16), (pins >> 8), pins])
        if mode == self.OUTPUT:
            self.write(_GPIO_BASE, _GPIO_DIRSET_BULK, cmd)
        elif mode == self.INPUT:
            self.write(_GPIO_BASE, _GPIO_DIRCLR_BULK, cmd)

        elif mode == self.INPUT_PULLUP:
            self.write(_GPIO_BASE, _GPIO_DIRCLR_BULK, cmd)
            self.write(_GPIO_BASE, _GPIO_PULLENSET, cmd)
            self.write(_GPIO_BASE, _GPIO_BULK_SET, cmd)

    def pin_mode_bulk_b(self, pins, mode):
        cmd = bytearray([0, 0, 0, 0, (pins >> 24), (pins >> 16), (pins >> 8), pins])
        if mode == self.OUTPUT:
            self.write(_GPIO_BASE, _GPIO_DIRSET_BULK, cmd)
        elif mode == self.INPUT:
            self.write(_GPIO_BASE, _GPIO_DIRCLR_BULK, cmd)

        elif mode == self.INPUT_PULLUP:
            self.write(_GPIO_BASE, _GPIO_DIRCLR_BULK, cmd)
            self.write(_GPIO_BASE, _GPIO_PULLENSET, cmd)
            self.write(_GPIO_BASE, _GPIO_BULK_SET, cmd)

    def digital_write_bulk(self, pins, value):
        cmd = bytearray([(pins >> 24), (pins >> 16), (pins >> 8), pins])
        if value:
            self.write(_GPIO_BASE, _GPIO_BULK_SET, cmd)
        else:
            self.write(_GPIO_BASE, _GPIO_BULK_CLR, cmd)


    def digital_write_bulk_b(self, pins, value):
        cmd = bytearray([0, 0, 0, 0, (pins >> 24), (pins >> 16), (pins >> 8), pins])
        if value:
            self.write(_GPIO_BASE, _GPIO_BULK_SET, cmd)
        else:
            self.write(_GPIO_BASE, _GPIO_BULK_CLR, cmd)

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
        cmd = bytearray([(baud >> 24), (baud >> 16), (baud >> 8), baud])
        self.write(_SERCOM0_BASE, _SERCOM_BAUD, cmd)

    def write8(self, reg_base, reg, value):
        self.write(reg_base, reg, bytearray([value]))

    def read8(self, reg_base, reg):
        ret = bytearray(1)
        self.read(reg_base, reg, ret)
        return ret[0]

    def read(self, reg_base, reg, buf, delay=.001):
        self.write(reg_base, reg)
        time.sleep(delay)
        with self.i2c_device as i2c:
            i2c.readinto(buf)

    def write(self, reg_base, reg, buf=None):
        full_buffer = bytearray([reg_base, reg])
        if buf is not None:
            full_buffer += buf

        with self.i2c_device as i2c:
            i2c.write(full_buffer)
