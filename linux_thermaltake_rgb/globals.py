"""
linux_thermaltake_rgb
Software to control your thermaltake hardware
Copyright (C) 2018  Max Chesterfield (chestm007@hotmail.com)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from enum import Enum

PROTOCOL_GET = 0x33
PROTOCOL_SET = 0x32

PROTOCOL_FAN = 0x51
PROTOCOL_LIGHT = 0x52


# credit: https://github.com/devcompl/riingplusapi
class RGB:
    class Mode:
        FLOW = 0x00
        SPECTRUM = 0x04
        RIPPLE = 0x08
        BLINK = 0x0c
        PULSE = 0x10
        WAVE = 0x14
        BY_LED = 0x18
        FULL = 0x19

    class Speed:
        SLOW = 0x03
        NORMAL = 0x02
        FAST = 0x01
        EXTREME = 0x00
