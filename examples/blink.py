from board import *
import busio
import Adafruit_seesaw
import time

myI2C = busio.I2C(SCL, SDA)

ss = Adafruit_seesaw.Seesaw(myI2C)

ss.pin_mode(15, ss.OUTPUT);


while True:
	ss.digital_write(15, True)   # turn the LED on (True is the voltage level)
	time.sleep(1)                # wait for a second
	ss.digital_write(15, False)  # turn the LED off by making the voltage LOW
	time.sleep(1)