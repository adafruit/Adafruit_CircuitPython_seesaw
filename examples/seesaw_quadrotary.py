# SPDX-FileCopyrightText: 2023 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Quad I2C rotary encoder NeoPixel color picker example."""
import board
from rainbowio import colorwheel
import digitalio
import adafruit_seesaw.seesaw
import adafruit_seesaw.neopixel
import adafruit_seesaw.rotaryio
import adafruit_seesaw.digitalio
import time

# For use with the STEMMA connector on QT Py RP2040
import busio
from adafruit_debug_i2c import DebugI2C

# For boards/chips that don't handle clock-stretching well, try running I2C at 50KHz
# i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
seesaw = adafruit_seesaw.seesaw.Seesaw(i2c, 0x49)

encoders = [adafruit_seesaw.rotaryio.IncrementalEncoder(seesaw, n) for n in range(4)]
switches = [adafruit_seesaw.digitalio.DigitalIO(seesaw, pin) for pin in (12, 14, 17, 9)]
for switch in switches:
    switch.switch_to_input(digitalio.Pull.UP)  # input & pullup!

# four neopixels per PCB
pixels = adafruit_seesaw.neopixel.NeoPixel(seesaw, 18, 4)
pixels.brightness = 0.5

last_positions = [-1, -1, -1, -1]
colors = [0, 0, 0, 0]  # start at red

while True:
    # negate the position to make clockwise rotation positive
    positions = [encoder.position for encoder in encoders]
    print(positions)
    continue
    for n, rotary_pos in enumerate(positions):
        if rotary_pos != last_positions[n]:
            print("Rotary #%d: %d" % (n, rotary_pos))
            last_positions[n] = rotary_pos

            if switches[n].value: # Change the LED color if switch is not pressed
                if rotary_pos > last_positions[n]:  # Advance forward through the colorwheel.
                    colors[n] += 8
                else:
                    colors[n] -= 8  # Advance backward through the colorwheel.
                colors[n] = (colors[n] + 256) % 256  # wrap around to 0-256

        # if switch is pressed, light up white, otherwise use the stored color
        if not switches[n].value:
           pixels[n] = 0xFFFFFF
        else:
           pixels[n] = colorwheel(colors[n])
