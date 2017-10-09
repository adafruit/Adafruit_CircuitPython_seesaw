from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
import time

SEESAW_STATUS_BASE = const(0x00)
SEESAW_GPIO_BASE = const(0x01)
SEESAW_SERCOM0_BASE = const(0x02)

SEESAW_TIMER_BASE = const(0x08)
SEESAW_ADC_BASE = const(0x09)
SEESAW_DAC_BASE = const(0x0A)
SEESAW_INTERRUPT_BASE = const(0x0B)
SEESAW_DAP_BASE = const(0x0C)
SEESAW_EEPROM_BASE = const(0x0D)
SEESAW_NEOPIXEL_BASE = const(0x0E)

SEESAW_GPIO_DIRSET_BULK = const(0x02)
SEESAW_GPIO_DIRCLR_BULK = const(0x03)
SEESAW_GPIO_BULK = const(0x04)
SEESAW_GPIO_BULK_SET = const(0x05)
SEESAW_GPIO_BULK_CLR = const(0x06)
SEESAW_GPIO_BULK_TOGGLE = const(0x07)
SEESAW_GPIO_INTENSET = const(0x08)
SEESAW_GPIO_INTENCLR = const(0x09)
SEESAW_GPIO_INTFLAG = const(0x0A)
SEESAW_GPIO_PULLENSET = const(0x0B)
SEESAW_GPIO_PULLENCLR = const(0x0C)

SEESAW_STATUS_HW_ID = const(0x01)
SEESAW_STATUS_VERSION = const(0x02)
SEESAW_STATUS_OPTIONS = const(0x03)
SEESAW_STATUS_SWRST = const(0x7F)

SEESAW_TIMER_STATUS = const(0x00)
SEESAW_TIMER_PWM = const(0x01)

SEESAW_ADC_STATUS = const(0x00)
SEESAW_ADC_INTEN = const(0x02)
SEESAW_ADC_INTENCLR = const(0x03)
SEESAW_ADC_WINMODE = const(0x04)
SEESAW_ADC_WINTHRESH = const(0x05)
SEESAW_ADC_CHANNEL_OFFSET = const(0x07)

SEESAW_SERCOM_STATUS = const(0x00)
SEESAW_SERCOM_INTEN = const(0x02)
SEESAW_SERCOM_INTENCLR = const(0x03)
SEESAW_SERCOM_BAUD = const(0x04)
SEESAW_SERCOM_DATA = const(0x05)

SEESAW_NEOPIXEL_STATUS = const(0x00)
SEESAW_NEOPIXEL_PIN = const(0x01)
SEESAW_NEOPIXEL_SPEED = const(0x02)
SEESAW_NEOPIXEL_BUF_LENGTH = const(0x03)
SEESAW_NEOPIXEL_BUF = const(0x04)
SEESAW_NEOPIXEL_SHOW = const(0x05)

ADC_INPUT_0_PIN = const(0x02)
ADC_INPUT_1_PIN  = const(0x03)
ADC_INPUT_2_PIN = const(0x04)
ADC_INPUT_3_PIN = const(0x05)

PWM_0_PIN = const(0x04)
PWM_1_PIN = const(0x05)
PWM_2_PIN = const(0x06)
PWM_3_PIN = const(0x07)

class Seesaw:

	INPUT = const(0x00)
	OUTPUT = const(0x01)
	INPUT_PULLUP = const(0x02)

	def __init__(self, i2c, addr=0x49):
		self.i2c_device = I2CDevice(i2c, addr)
		self.begin()

	def begin(self):
		self.sw_reset()
		time.sleep(.500)

		c = self.read8(SEESAW_STATUS_BASE, SEESAW_STATUS_HW_ID)

		if c != 0x55:
			print(c)
			raise RuntimeError("Seesaw hardware ID returned is not correct! Please check your wiring.")

	def sw_reset(self):

		self.write8(SEESAW_STATUS_BASE, SEESAW_STATUS_SWRST, 0xFF)

	def get_options(self):

		buf = bytearray(4)
		self.read(SEESAW_STATUS_BASE, SEESAW_STATUS_OPTIONS, buf, 4)
		ret = (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3]
		return ret

	def get_version(self):

		buf = bytearray(4)
		self.read(SEESAW_STATUS_BASE, SEESAW_STATUS_VERSION, buf, 4)
		ret = (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3]
		return ret

	def pin_mode(self, pin,  mode):

		self.pin_mode_bulk(1 << pin, mode)


	def digital_write(self, pin,  value):

		self.digital_write_bulk(1 << pin, value)


	def digital_read(self, pin):

		return self.digital_read_bulk((1 << pin)) != 0


	def digital_read_bulk(self, pins):

		buf = bytearray(4)
		self.read(SEESAW_GPIO_BASE, SEESAW_GPIO_BULK, buf)
		ret = ( (buf[0] & 0xF) << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3] #TODO: weird overflow error, fix
		return ret & pins


	def set_GPIO_interrupts(self, pins, enabled):

		cmd =  bytearray([(pins >> 24) , (pins >> 16), (pins >> 8), pins])
		if enabled:
			self.write(SEESAW_GPIO_BASE, SEESAW_GPIO_INTENSET, cmd)
		else:
			self.write(SEESAW_GPIO_BASE, SEESAW_GPIO_INTENCLR, cmd)


	def analog_read(self, pin):

		buf = bytearray(2)

		if pin == ADC_INPUT_0_PIN:
			p = 0
		elif pin == ADC_INPUT_1_PIN:
			p = 1
		elif pin == ADC_INPUT_2_PIN: 
			p = 2
		elif pin == ADC_INPUT_3_PIN: 
			p = 3
		else:
			return 0

		self.read(SEESAW_ADC_BASE, SEESAW_ADC_CHANNEL_OFFSET + p, buf)
		ret = (buf[0] << 8) | buf[1]
		time.sleep(.001)
		return ret


	def pin_mode_bulk(self, pins, mode):

		cmd =  bytearray([(pins >> 24) , (pins >> 16), (pins >> 8), pins ])

		if mode == self.OUTPUT:
			self.write(SEESAW_GPIO_BASE, SEESAW_GPIO_DIRSET_BULK, cmd)
			
		elif mode == self.INPUT:
			self.write(SEESAW_GPIO_BASE, SEESAW_GPIO_DIRCLR_BULK, cmd)
			
		elif mode == self.INPUT_PULLUP:
			self.write(SEESAW_GPIO_BASE, SEESAW_GPIO_DIRCLR_BULK, cmd)
			self.write(SEESAW_GPIO_BASE, SEESAW_GPIO_PULLENSET, cmd)
			self.write(SEESAW_GPIO_BASE, SEESAW_GPIO_BULK_SET, cmd)
			

	def digital_write_bulk(self, pins, value):

		cmd =  bytearray([(pins >> 24) , (pins >> 16), (pins >> 8), pins])
		if value:
			self.write(SEESAW_GPIO_BASE, SEESAW_GPIO_BULK_SET, cmd)
		else:
			self.write(SEESAW_GPIO_BASE, SEESAW_GPIO_BULK_CLR, cmd)


	def analog_write(self, pin, value):

		p = -1
		if pin == PWM_0_PIN:
			p = 0 
		elif pin == PWM_1_PIN:
			p = 1 
		elif pin == PWM_2_PIN:
			p = 2 
		elif pin == PWM_3_PIN:
			p = 3

		if p > -1:
			cmd = bytearray([p, value])
			self.write(SEESAW_TIMER_BASE, SEESAW_TIMER_PWM, cmd)

	"""
	def enable_sercom_data_rdy_interrupt(self, sercom):

		_sercom_inten.DATA_RDY = 1
		self.write8(SEESAW_SERCOM0_BASE + sercom, SEESAW_SERCOM_INTEN, _sercom_inten.get())


	def disable_sercom_data_rdy_interrupt(self, sercom):

		_sercom_inten.DATA_RDY = 0
		self.write8(SEESAW_SERCOM0_BASE + sercom, SEESAW_SERCOM_INTEN, _sercom_inten.get())


	def read_sercom_data(self, sercom):

		return self.read8(SEESAW_SERCOM0_BASE + sercom, SEESAW_SERCOM_DATA)
	"""

	def set_i2c_addr(self, addr):

		self.eeprom_write8(SEESAW_EEPROM_I2C_ADDR, addr)
		time.sleep(.250)
		self.begin(addr) #restart w/ the new addr


	def get_i2c_addr(self,):

		return self.read8(SEESAW_EEPROM_BASE, SEESAW_EEPROM_I2C_ADDR)


	def eeprom_write8(self, addr,  val):
		self.eeprom_write(addr, bytearray([val]))


	def eeprom_write(self, addr,  buf):

		self.write(SEESAW_EEPROM_BASE, addr, buf)


	def eeprom_read8(self, addr):

		return self.read8(SEESAW_EEPROM_BASE, addr)


	def uart_set_baud(self, baud):

		cmd = bytearray([(baud >> 24), (baud >> 16), (baud >> 8), baud])
		self.write(SEESAW_SERCOM0_BASE, SEESAW_SERCOM_BAUD, cmd)


	def write8(self, regHigh, regLow, value):

		self.write(regHigh, regLow, bytearray([value]))


	def read8(self, regHigh, regLow):

		ret = bytearray(1)
		self.read(regHigh, regLow, ret)

		return ret[0]


	def read(self, regHigh,  regLow,  buf, delay=.001):
		self.write(regHigh, regLow)
		time.sleep(delay)
		with self.i2c_device as i2c:
			i2c.read_into(buf)


	def write(self, regHigh,  regLow, buf = None):
		c = bytearray([regHigh, regLow])
		if not buf == None:
			c = c + buf

		with self.i2c_device as i2c:
			i2c.write(c)