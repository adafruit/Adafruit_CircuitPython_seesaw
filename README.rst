
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-seesaw/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/seesaw/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_seesaw/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_seesaw/actions
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython module for use with the Adafruit ATSAMD09 seesaw.

Experimental STM32C011 support
-----------------------------

The provisional hardware ID 0x90 selects the STM32C011 pin map. Pins 0..8 are
PA0..PA8, 9 is PA11, 10 is PA12, and 15 is PC14. Enabled firmware features
reserve their pins. Native ``analog_read()`` values are 12-bit;
``AnalogInput.value`` scales these into its 16-bit domain. Existing chips keep
their previous behavior. The EEPROM I2C-address byte is 0xFF.

``adafruit_seesaw.spi.SPIBridge`` provides chunked transfers with held CS for
the experimental SPI-enabled C011 firmware. See ``examples/seesaw_spi_bridge.py``.
It is not a drop-in ``busio.SPI`` replacement or an integrated e-paper driver.
Development testing runs this Python driver on CPython through physical Metro
I2C; native CircuitPython runtime testing remains outstanding.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-seesaw/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-seesaw

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-seesaw

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-seesaw

Usage Example
=============

See examples/seesaw_simpletest.py for usage example.

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/seesaw/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_seesaw/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
