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
from collections import namedtuple

from linux_thermaltake_rgb import LOGGER
from linux_thermaltake_rgb.classified_object import ClassifiedObject
from linux_thermaltake_rgb.globals import PROTOCOL_SET, PROTOCOL_LIGHT, PROTOCOL_FAN, PROTOCOL_GET

FanSpeed = namedtuple('FanSpeed', ['set_speed', 'rpm'])


class ThermaltakeDevice(ClassifiedObject):
    model = None

    def __init__(self, controller, port: int):
        self.port = int(port)
        self.controller = controller

    @classmethod
    def factory(cls, model, controller, port):
        subclass_dict = {clazz.model.lower(): clazz for clazz in cls.inheritors() if clazz.model is not None}
        try:
            return subclass_dict[model.lower()](controller, port)
        except KeyError:
            LOGGER.warn(f'model {model} not found. controller: {controller} port: {port}')


class ThermaltakeRGBDevice(ThermaltakeDevice):
    num_leds = 0
    index_per_led = 0

    def set_lighting(self, values: list = None, mode=0x18, speed=0x00) -> None:
        """
        for the sake of performance this will assume the data your passing in is correct.
        if it isnt the worst that will happen (i guess) is the lights wont show up as
        expected.
        :param values: [r,g,b...]
        :param mode: lighting mode(hex)
        :param speed: light update speed(hex)
        """
        data = [PROTOCOL_SET, PROTOCOL_LIGHT, self.port, mode + speed]
        if values:
            data.extend(values)
        LOGGER.debug(data)
        self.controller.driver.write_out(data)


class ThermaltakeFanDevice(ThermaltakeDevice):
    def set_fan_speed(self, speed: int):
        data = [PROTOCOL_SET, PROTOCOL_FAN, self.port, 0x01, int(speed)]
        self.controller.driver.write_out(data)

    def get_fan_speed(self):
        data = [PROTOCOL_GET, PROTOCOL_FAN, self.port]
        self.controller.driver.write_out(data)
        id, unknown, speed, rpm_l, rpm_h = self.controller.driver.read_in()[2:7]
        return FanSpeed(speed, (rpm_h << 8) + rpm_l)


from linux_thermaltake_rgb.devices.pumps import *
from linux_thermaltake_rgb.devices.fans import *
from linux_thermaltake_rgb.devices.lights import *
