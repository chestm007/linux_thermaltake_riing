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
from linux_thermaltake_rgb import LOGGER
from linux_thermaltake_rgb.devices import ThermaltakeRGBDevice
from linux_thermaltake_rgb.drivers import ThermaltakeiRGBPLUSControllerDriver


class ThermaltakePSUDevice(ThermaltakeRGBDevice):
    model = 'iRGBPlus'
    num_leds = 12
    index_per_led = 3

    def __init__(self, controller=None, port=None):
        self.driver = ThermaltakeiRGBPLUSControllerDriver()

    def set_lighting(self, values: list = None, mode=0x18, speed=0x00):
        data = [0x30, 0x42, mode]
        if values:
            data.extend(values)
        LOGGER.debug('{} set lighting: raw hex: {}'.format(self.__class__.__name__, data))
        self.driver.write_out(data)
