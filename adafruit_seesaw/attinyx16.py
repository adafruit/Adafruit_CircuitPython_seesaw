class ATtinyx16_Pinmap:
    """This class is automatically used by `adafruit_seesaw.seesaw.Seesaw` when
    a ATtinyx16 Breakout (PID 5690, PID 5681) is detected.

    It is also a reference for the capabilities of each pin."""

    #: The pins capable of analog output
    analog_pins = (0, 1, 2, 3, 4, 5, 14, 15, 16)

    """The effective bit resolution of the PWM pins"""
    pwm_width = 16  # we dont actually use all 16 bits but whatever

    """The pins capable of PWM output"""
    pwm_pins = (0, 1, 7, 11, 16)

    """No pins on this board are capable of touch input"""
    touch_pins = ()
