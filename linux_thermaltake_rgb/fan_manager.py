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

from linux_thermaltake_rgb import LOGGER
from linux_thermaltake_rgb.classified_object import ClassifiedObject


class FanModel(ClassifiedObject):
    @classmethod
    def factory(cls, config):
        subclass_dict = {clazz.model: clazz for clazz in cls.inheritors()}
        try:
            return subclass_dict.get(config.pop('model').lower())(config)
        except KeyError as e:
            LOGGER.warn('%s not found in config item', e)

    def main(self):
        """
        returns an integer between 0 and 100 to set the fan speed too
        """
        raise NotImplementedError


class TempTargetModel(FanModel):
    model = 'temp_target'

    def __init__(self, config):
        self.sensor_name = config.get('sensor_name')
        self.target = float(config.get('target'))
        self.multiplier = config.get('multiplier')
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
    model = 'locked_speed'

    def __init__(self, config):
        speed = config.get('speed')
        if not 0 <= speed <= 100:
            raise ValueError(f'Speed must be between 0 and 100, got {speed}')
        self.speed = speed

    def main(self):
        LOGGER.debug(f'Setting fan speed to {self.speed}%')
        return self.speed

    def __str__(self) -> str:
        return f'locked speed {self.speed}%'


class CurveModel(FanModel):
    """
    creates a fan curve based on user defined points
    """
    model = 'curve'

    def __init__(self, config):
        self.points = np.array(config.get('points'))
        self.temps = self.points[:, 0]
        self.speeds = self.points[:, 1]
        self.sensor_name = config.get('sensor_name')
        LOGGER.debug(f'curve fan points: {self.points}')

        if np.min(self.speeds) < 0:
            raise ValueError(f'Fan curve contains negative speeds, speed should be in [0,100]')
        if np.max(self.speeds) > 100:
            raise ValueError(f'Fan curve contains speeds greater than 100, speed should be in [0,100]')
        if np.any(np.diff(self.temps) <= 0):
            raise ValueError(f'Fan curve points should be strictly monotonically increasing, configuration error ?')
        if np.any(np.diff(self.speeds) < 0):
            raise ValueError(f'Curve fan speeds should be monotonically increasing, configuration error ?')

    def main(self):
        """
        returns a speed for a given temperature
        :return:
        """
        return np.interp(x=self._get_temp(), xp=self.temps, fp=self.speeds)

    def _get_temp(self):
        return sensors_temperatures().get(self.sensor_name)[0].current

    def __str__(self) -> str:
        return f'curve {self.points}'


class FanManager:
    def __init__(self, initial_model: FanModel=None):
        self._continue = False
        self._thread = Thread(target=self._main_loop)
        self._devices = []
        self._model = initial_model
        LOGGER.debug(f'creating FanManager object: [model: {initial_model}]')

    def attach_device(self, device):
        self._devices.append(device)

    def set_controller(self, model: FanModel):
        LOGGER.debug(f'setting fan model: {model.__class__.__name__}')
        if isinstance(model, FanModel):
            LOGGER.debug(f'SUCCESS: set fan model: {model.__class__.__name__}')
            self._model = model

    def _main_loop(self):
        LOGGER.debug(f'entering {self.__class__.__name__} main loop')
        last_speed = None
        while self._continue:
            speed = int(round(self._model.main()))
            if last_speed != speed:
                last_speed = speed
                LOGGER.debug(f'new fan speed {speed}')
                for dev in self._devices:
                    dev.set_fan_speed(speed)
            time.sleep(1)
        LOGGER.debug(f'exiting {self.__class__.__name__} main loop')

    def start(self):
        LOGGER.info(f'Starting fan manager ({self._model})...')
        self._continue = True
        self._thread.start()

    def stop(self):
        LOGGER.info(f'Stopping fan manager...')
        self._continue = False
        self._thread.join()
