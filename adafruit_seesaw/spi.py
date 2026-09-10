# SPDX-FileCopyrightText: 2026 Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Experimental I2C-to-SPI controller bridge with chunked, CS-held transfers.

This is a bridge API, not a drop-in ``busio.SPI`` replacement. C011 uses
PA4 for CS, PA5 for SCK, PA6 for MISO, and PA7 for MOSI. Display D/C, reset,
and BUSY can use separate seesaw GPIOs.
"""

import struct
import time

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_seesaw.git"

_BASE = 0x13
_STATUS = 0x00
_CONFIG = 0x01
_TRANSFER = 0x02
_READ = 0x03
_ABORT = 0x04
_CLOCK = 0x05
_BUSY = 0x01
_READY = 0x02
_BEGIN = 0x01
_END = 0x02
_DISCARD = 0x04
_CHUNK = 29
_TIMEOUT = 0.25


class SPIBridge:
    """SPI controller accessed through an initialized :class:`Seesaw` object.

    :param seesaw: Initialized seesaw peripheral with the SPI option enabled.
    """

    def __init__(self, seesaw):
        self._seesaw = seesaw

    def _wait(self):
        """Wait for completion, reporting device and transport failures."""
        status = bytearray(4)
        started = time.monotonic()
        while True:
            self._seesaw.read(_BASE, _STATUS, status, 0.0001)
            if not status[0] & _BUSY:
                if status[1]:
                    raise RuntimeError(f"seesaw SPI error {status[1]}")
                return status
            if time.monotonic() - started >= _TIMEOUT:
                raise RuntimeError("seesaw SPI completion timed out")
            time.sleep(0.001)

    def configure(self, frequency=1000000, mode=0, lsb_first=False):
        """Configure SPI, releasing any previous transaction first.

        :param int frequency: Maximum clock in Hz, 187500..24000000 on C011.
        :param int mode: SPI mode 0, 1, 2, or 3.
        :param bool lsb_first: False for MSB first, True for LSB first.
        The clock is rounded down to a hardware divisor; use ``clock_frequency``
        for the actual setting. All four SPI pins are reserved until ``abort()``.
        """
        if not 187500 <= frequency <= 24000000 or not 0 <= mode <= 3:
            raise ValueError("Unsupported SPI frequency or mode")
        if not self._seesaw.get_options() & (1 << _BASE):
            raise RuntimeError("The seesaw SPI controller option is not enabled")
        self.abort()
        self._seesaw.write(_BASE, _CONFIG, struct.pack(">BBI", mode, bool(lsb_first), frequency))
        if not self._wait()[0] & _READY:
            raise RuntimeError("The seesaw SPI controller did not become ready")

    @property
    def clock_frequency(self):
        """Actual SPI clock in Hz, or zero when the controller is disabled."""
        value = bytearray(4)
        self._seesaw.read(_BASE, _CLOCK, value, 0.0001)
        return struct.unpack(">I", value)[0]

    def transfer(self, tx=None, rx=None, *, begin=True, end=True):
        """Transfer buffers, automatically splitting them into 29-byte chunks.

        :param tx: Transmit bytes, or None to transmit 0xFF while receiving.
        :param rx: Receive buffer, or None to discard receive bytes.
        :param bool begin: Assert CS before the first chunk.
        :param bool end: Release CS after the last chunk.
        Length is taken from tx when provided, otherwise rx. Both None clocks
        no bytes, allowing explicit CS transitions. To change display D/C while
        CS is held, finish one call with end=False and continue with begin=False.

        Errors raise an exception and attempt to disable the bridge. A broken
        I2C connection can prevent cleanup; restore communication before assuming
        the peripheral is idle.
        """
        length = len(tx) if tx is not None else len(rx) if rx is not None else 0
        if rx is not None and len(rx) < length:
            raise ValueError("Receive buffer is shorter than transmit buffer")
        try:
            self._transfer_chunks(tx, rx, length, begin, end)
        except (OSError, RuntimeError):
            try:
                self.abort()
            except (OSError, RuntimeError):
                pass  # Preserve the original failure; cleanup is best effort.
            raise

    def _transfer_chunks(self, tx, rx, length, begin, end):
        """Send bounded chunks, checking completion before reading each result."""
        view = memoryview(rx) if rx is not None else None
        offset = 0
        first = True
        while first or offset < length:
            first = False
            sequence = self._wait()[3]
            count = min(_CHUNK, length - offset)
            packet = bytearray(count + 1)
            if rx is None:
                packet[0] |= _DISCARD
            if offset == 0 and begin:
                packet[0] |= _BEGIN
            if offset + count == length and end:
                packet[0] |= _END
            for index in range(count):
                packet[index + 1] = tx[offset + index] if tx is not None else 0xFF
            self._seesaw.write(_BASE, _TRANSFER, packet)
            status = self._wait()
            expected_rx = count if rx is not None else 0
            if status[3] != (sequence + 1) & 0xFF or status[2] != expected_rx:
                raise RuntimeError("Unexpected SPI completion sequence or receive length")
            if count and view is not None:
                self._seesaw.read(_BASE, _READ, view[offset : offset + count], 0.0001)
            offset += count

    def abort(self, release_pins=True):
        """Release CS and clear errors/RX; normally also return SPI pins to inputs."""
        self._seesaw.write8(_BASE, _ABORT, int(release_pins))
        self._wait()
