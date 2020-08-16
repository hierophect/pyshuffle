# The MIT License (MIT)
#
# Copyright (c) 2019 Scott Shawcroft for Adafruit Industries LLC
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
`adafruit_il0398`
================================================================================
CircuitPython displayio drivers for IL0398 driven e-paper displays
* Author(s): Scott Shawcroft
Implementation Notes
--------------------
**Hardware:**
**Software and Dependencies:**
* Adafruit CircuitPython (5+) firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_IL0398.git"

# TODO: Try LUTs from:
# https://github.com/waveshare/e-Paper/blob/master/STM32/STM32-F103ZET6/User/e-Paper/EPD_4in2.c

_START_SEQUENCE = (
    b"\x01\x04\x03\x00\x2b\x2b"  # power setting
    b"\x06\x03\x17\x17\x17"  # booster soft start
    b"\x04\x80\xc8"  # power on and wait 200 ms
    b"\x00\x01\x0f"  # panel setting
    b"\x61\x04\x00\x00\x00\x00"  # Resolution
)

_STOP_SEQUENCE = (
    b"\x50\x01\xf7"  # CDI setting
    b"\x02\x80\xf0"  # Power off
    # TODO: Busy wait
    # b"\x07\x01\xa5" # Deep sleep
)

# pylint: disable=too-few-public-methods
class IL0398(displayio.EPaperDisplay):
    """IL0398 driver"""

    def __init__(self, bus, **kwargs):
        start_sequence = bytearray(_START_SEQUENCE)

        width = kwargs["width"]
        height = kwargs["height"]
        if "rotation" in kwargs and kwargs["rotation"] % 180 != 0:
            width, height = height, width
        start_sequence[-4] = (width >> 8) & 0xFF
        start_sequence[-3] = width & 0xFF
        start_sequence[-2] = (height >> 8) & 0xFF
        start_sequence[-1] = height & 0xFF
        if "highlight_color" in kwargs:
            write_black_ram_command = 0x10
            write_color_ram_command = 0x13
        else:
            write_color_ram_command = 0x10
            write_black_ram_command = 0x13
        super().__init__(
            bus,
            start_sequence,
            _STOP_SEQUENCE,
            **kwargs,
            ram_width=400,
            ram_height=300,
            busy_state=False,
            write_black_ram_command=write_black_ram_command,
            write_color_ram_command=write_color_ram_command,
            color_bits_inverted=True,
            refresh_display_command=0x12,
            seconds_per_frame=5,
        )