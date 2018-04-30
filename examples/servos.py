from board import SCL, SDA
import busio
import adafruit_seesaw
from adafruit_motor import servo

from analogio import AnalogOut
import board

i2c_bus = busio.I2C(SCL, SDA)

ss = adafruit_seesaw.Seesaw(i2c_bus)

pwm1 = ss.get_pwm(17)
pwm2 = ss.get_pwm(16)
pwm3 = ss.get_pwm(15)
pwm4 = ss.get_pwm(14)

pwm1.frequency = 50

S1 = servo.Servo(pwm1)
S2 = servo.Servo(pwm2)
S3 = servo.Servo(pwm3)
S4 = servo.Servo(pwm4)

S1.angle = 180
S2.angle = 50
S3.angle = 25
S4.angle = 75