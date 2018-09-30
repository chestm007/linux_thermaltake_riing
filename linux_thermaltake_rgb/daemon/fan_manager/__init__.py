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

from psutil import sensors_temperatures

from linux_thermaltake_rgb import LOGGER


def fan_controller_factory(type=None, *args, **kwargs):
    if type == 'locked_speed':
        return LockedSpeedController(*args, **kwargs)
    elif type == 'temp_target':
        return TempTargetController(*args, **kwargs)


class FanController:
    def main(self):
        """
        returns an integer between 0 and 100 to set the fan speed too
        """
        raise NotImplementedError


class TempTargetController(FanController):
    def __init__(self, target, sensor_name, multiplier: int = 5):
        self.sensor_name = sensor_name
        self.target = float(target)
        self.multiplier = multiplier
        self.last_speed = 10

    def main(self):
        temp = self._get_temp()
        speed = (((temp - self.target) * self.multiplier) + self.last_speed) / 2

        if speed < 0:
            speed = 0
        elif speed > 100:
            speed = 100

        LOGGER.debug(f'Temperature is {temp}°C, setting fan speed to {speed}%')
        return speed

    def _get_temp(self):
        return sensors_temperatures().get(self.sensor_name)[0].current

    def __str__(self) -> str:
        return f'target {self.target}°C on sensor {self.sensor_name}'


class LockedSpeedController(FanController):
    def __init__(self, speed):
        if not 0 <= speed <= 100:
            raise ValueError(f'Speed must be between 0 and 100, got {speed}')
        self.speed = speed

    def main(self):
        LOGGER.debug(f'Setting fan speed to {self.speed}%')
        return self.speed

    def __str__(self) -> str:
        return f'locked speed {self.speed}%'


class FanManager:
    def __init__(self, initial_controller: FanController = None):
        self._continue = False
        self._thread = Thread(target=self._main_loop)
        self._devices = []
        self._controller = initial_controller

    def attach_device(self, device):
        self._devices.append(device)

    def set_controller(self, controller: FanController):
        if isinstance(controller, FanController):
            self._controller = controller

    def _main_loop(self):
        while self._continue:
            speed = self._controller.main()
            for dev in self._devices:
                dev.set_fan_speed(speed)
            time.sleep(5)

    def start(self):
        LOGGER.info(f'Starting fan manager ({self._controller})...')
        self._continue = True
        self._thread.start()

    def stop(self):
        LOGGER.info(f'Stopping fan manager...')
        self._continue = False
        self._thread.join()
