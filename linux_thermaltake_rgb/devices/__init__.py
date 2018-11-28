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
from linux_thermaltake_rgb.globals import PROTOCOL_SET, PROTOCOL_LIGHT, PROTOCOL_FAN, PROTOCOL_GET

FLOE_RIING_RGB = 'Floe Riing RGB'
RIING_PLUS = 'Riing Plus'
PR22D5_PLUS = 'Pacific PR22-D5 Plus'
W4_PLUS = 'Pacific W4 Plus CPU Waterblock'
VGTX_1080_PLUS = 'Pacific V-GTX 1080Ti Plus GPU Waterblock'
RAD_PLUS = 'Pacific Rad Plus LED Panel'
LUMI_PLUS = 'Lumi Plus LED Strip'


class ThermaltakeDevice:
    def __init__(self, controller, port: int):
        self.port = int(port)
        self.controller = controller


class ThermaltakeRGBDevice(ThermaltakeDevice):
    num_leds = 0
    index_per_led = 0

    def set_lighting(self, values: list) -> None:
        """
        for the sake of performance this will assume the data your passing in is correct.
        if it isnt the worst that will happen (i guess) is the lights wont show up as
        expected.
        :param values: [r,g,b...]
        """
        data = [PROTOCOL_SET, PROTOCOL_LIGHT, self.port, 0x18]
        data.extend(values)
        self.controller.driver.write_out(data)


class ThermaltakeFanDevice(ThermaltakeDevice):
    def set_fan_speed(self, speed: int):
        data = [PROTOCOL_SET, PROTOCOL_FAN, self.port, 0x01, int(speed)]
        self.controller.driver.write_out(data)

    def get_fan_speed(self):
        data = [PROTOCOL_GET, PROTOCOL_FAN, self.port]
        self.controller.driver.write_out(data)
        self.controller.driver.read_in()



