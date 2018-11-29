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
from linux_thermaltake_rgb.devices import ThermaltakeRGBDevice


class ThermaltakePR22D5Res(ThermaltakeRGBDevice):
    model = 'Pacific PR22-D5 Plus'
    num_leds = 12
    index_per_led = 3


class ThermaltakeW4PlusWB(ThermaltakeRGBDevice):
    model = 'Pacific W4 Plus CPU Waterblock'
    num_leds = 12
    index_per_led = 3


class ThermaltakeVGTX1080PlusWB(ThermaltakeRGBDevice):
    model = 'Pacific V-GTX 1080Ti Plus GPU Waterblock'
    num_leds = 12
    index_per_led = 3


class ThermaltakeRadPlusLED(ThermaltakeRGBDevice):
    model = 'Pacific Rad Plus LED Panel'
    num_leds = 12
    index_per_led = 3


class ThermaltakeLumiPlusLED(ThermaltakeRGBDevice):
    model = 'Lumi Plus LED Strip'
    num_leds = 12
    index_per_led = 3
