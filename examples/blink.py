import time

from board import SCL, SDA
import busio
import adafruit_seesaw

i2c_bus = busio.I2C(SCL, SDA)

ss = adafruit_seesaw.Seesaw(i2c_bus)

ss.pin_mode(15, ss.OUTPUT)

while True:
    ss.digital_write(15, True)   # turn the LED on (True is the voltage level)
    time.sleep(1)                # wait for a second
    ss.digital_write(15, False)  # turn the LED off by making the voltage LOW
    time.sleep(1)
