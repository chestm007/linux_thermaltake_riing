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
import time
from threading import Thread


def lighting_controller_factory(**kwargs):
    args = dict(kwargs)
    _type = args.pop('type')
    if _type == 'static':
        return StaticLightingController(**args)


class LightingController:
    def main(self, device):
        """
        returns a hex array to set the lights too
        """
        raise NotImplementedError


class StaticLightingController(LightingController):
    def __init__(self, r: int, g: int, b: int):
        self.r, self.g, self.b = r, g, b

    def main(self, device) -> list:
        data = []
        if device.index_per_led == 3:
            for i in range(device.num_leds):
                data.extend([self.g, self.r, self.b])
        return data


class LightingManager:
    def __init__(self, initial_controller: LightingController=None):
        self._continue = False
        self._thread = Thread(target=self._main_loop)
        self._devices = []
        self._controller = initial_controller

    def attach_device(self, device):
        self._devices.append(device)

    def _main_loop(self):
        while self._continue:
            for dev in self._devices:
                lights = self._controller.main(dev)
                dev.set_lighting(lights)
            time.sleep(0.05)

    def start(self):
        self._continue = True
        if self._controller is None:
            self._controller = LightingController()
        self._thread.start()

    def stop(self):
        self._continue = False
        self._thread.join()
