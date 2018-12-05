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

import numpy as np
from psutil import sensors_temperatures
from scipy.interpolate import pchip
from matplotlib import pyplot

from linux_thermaltake_rgb import LOGGER


def fan_model_factory(model=None, *args, **kwargs):
    if model == 'locked_speed':
        return LockedSpeedModel(*args, **kwargs)
    elif model == 'temp_target':
        return TempTargetModel(*args, **kwargs)
    elif model == 'curve':
        return CurveModel(*args, **kwargs)


class FanModel:
    def main(self):
        """
        returns an integer between 0 and 100 to set the fan speed too
        """
        raise NotImplementedError


class TempTargetModel(FanModel):
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


class LockedSpeedModel(FanModel):
    def __init__(self, speed):
        if not 0 <= speed <= 100:
            raise ValueError(f'Speed must be between 0 and 100, got {speed}')
        self.speed = speed

    def main(self):
        LOGGER.debug(f'Setting fan speed to {self.speed}%')
        return self.speed

    def __str__(self) -> str:
        return f'locked speed {self.speed}%'


class CurveModel:
    """
    creates a fan curve based on user defined points
    """
    def __init__(self, points: list=None):
        self.points = points
        LOGGER.debug(f'curve fan points: {self.points}')
        # ensure the curve starts at 0, 0
        has_zero = False
        for point in self.points:
            if point[0] == 0:
                has_zero = True

        if not has_zero:
            self.points.insert(0, [0, 0])

        self.points.sort(key=lambda s: s[0])

        temps = []
        speeds = []
        for set_ in points:
            temps.append(set_[0])
            speeds.append(set_[1])

        self._array = []

        # this involved alot of stack overflow and admittedly im not 100% sure how it works
        # basically given a set of points it extrapolates that into a line consisting of one
        # point per degree.
        x = np.asarray(temps)
        y = np.asarray(speeds)
        pch = pchip(x, y)
        xx = np.linspace(x[0], x[-1], x[-1])
        line2d = pyplot.plot(xx, pch(xx), 'g-')
        self.temps = line2d[0].get_xdata()
        self.speeds = line2d[0].get_ydata()

    def main(self, temp):
        """
        returns a speed for a given temperature
        :param temp: int
        :return:
        """
        if temp > len(self.speeds):
            temp = len(self.speeds)
        if temp <= 0:
            temp = 1
            LOGGER.debug(f'setting speed to {self.speeds[temp - 1]}')
        return self.speeds[temp - 1]

    def __str__(self) -> str:
        return f'curve {self.points}'


class FanManager:
    def __init__(self, initial_model: FanModel = None):
        self._continue = False
        self._thread = Thread(target=self._main_loop)
        self._devices = []
        self._model = initial_model

    def attach_device(self, device):
        self._devices.append(device)

    def set_controller(self, model: FanModel):
        if isinstance(model, FanModel):
            self._model = model

    def _main_loop(self):
        while self._continue:
            speed = self._model.main()
            for dev in self._devices:
                dev.set_fan_speed(speed)
            time.sleep(5)

    def start(self):
        LOGGER.info(f'Starting fan manager ({self._model})...')
        self._continue = True
        self._thread.start()

    def stop(self):
        LOGGER.info(f'Stopping fan manager...')
        self._continue = False
        self._thread.join()
