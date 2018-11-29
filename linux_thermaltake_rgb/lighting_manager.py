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
from collections import namedtuple
from threading import Thread

from psutil import sensors_temperatures

from linux_thermaltake_rgb import LOGGER
from linux_thermaltake_rgb.classified_object import ClassifiedObject
from linux_thermaltake_rgb.globals import RGB
import math


def compass_to_rgb(h, s=1, v=1):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f

    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q

    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return g, r, b


class LightingEffect(ClassifiedObject):
    model = None

    def __init__(self, config):
        self._config = config
        self._devices = []
        LOGGER.info(f'initializing {self.__class__.__name__} light controller')

    @classmethod
    def factory(cls, config):
        subclass_dict = {clazz.model: clazz for clazz in cls.inheritors()}
        try:
            return subclass_dict.get(config.pop('model').lower())(config)
        except KeyError as e:
            LOGGER.warn('%s not found in config item', e)

    def attach_device(self, device):
        self._devices.append(device)

    def start(self):
        raise NotImplementedError

    def stop(self):
        return


class CustomLightingEffect(LightingEffect):
    SLOW = 1
    NORMAL = 0.75
    FAST = 0.5
    EXTREME = 0.25

    def __init__(self, config):
        super().__init__(config)
        conf_speed = self._config.get('speed', 'normal')
        self._speed = getattr(self, conf_speed.upper())

    def start(self):
        raise NotImplementedError


class ThreadedCustomLightingEffect(CustomLightingEffect):
    def __init__(self, config):
        super().__init__(config)
        self._continue = False
        self._thread = Thread(target=self._main_loop)

    def start(self):
        self._continue = True
        self._thread.start()

    def stop(self):
        self._continue = False
        self._thread.join()

    def begin_all(self):
        pass

    def _main_loop(self):
        self.begin_all()
        while self._continue:
            self.next()
            time.sleep(self._speed)

    def next(self):
        raise NotImplementedError


class AlternatingLightingEffect(CustomLightingEffect):
    """
    ::: settings: [odd_rgb:{r,g,b}, even_rgb:{r,g,b}]
    """
    model = 'alternating'
    RGBMap = namedtuple('RGBMap', ['g', 'r', 'b'])

    def __init__(self, config):
        super().__init__(config)
        self.odd_rgb = self.RGBMap(**self._config.get('odd_rgb'))
        self.even_rgb = self.RGBMap(**self._config.get('even_rgb'))

    def start(self):
        for dev in self._devices:
            values = []
            for i in range(dev.num_leds):
                if i % 2 == 0:
                    values.extend(self.even_rgb)
                else:
                    values.extend(self.odd_rgb)
            dev.set_lighting(values=values)

    def __str__(self) -> str:
        return f'alternating lighting {self.odd_rgb} {self.even_rgb}'


class TemperatureLightingEffect(ThreadedCustomLightingEffect):
    """
    ::: settings: [speed, cold, hot, target, sensor_name]
    """
    model = 'temperature'

    cold_angle = 240
    target_angle = 120
    hot_angle = 0

    def __init__(self, config):
        super().__init__(config)
        self.sensor_name = self._config.get('sensor_name')
        self.cold = int(self._config.get('cold', 20))
        self.target = int(self._config.get('target', 30))
        self.hot = int(self._config.get('hot', 60))
        self.cur_temp = 0
        self.angle = 0

    def next(self):
        def flatten(l):
            return [item for sublist in l for item in sublist]

        self.cur_temp = sensors_temperatures().get(self.sensor_name)[0].current
        if self.cur_temp <= self.cold:
            self.angle = self.cold_angle
        elif self.cur_temp < self.target:
            self.angle = ((self.cold_angle - self.target_angle)
                          / (self.target - self.cold)
                          * (self.target - self.cur_temp))
        elif self.cur_temp == self.target:
            self.angle = self.target_angle
        elif self.cur_temp > self.hot:
            self.angle = self.hot_angle
        elif self.cur_temp > self.target:
            self.angle = 120 - ((self.target_angle - self.hot_angle)
                                / (self.hot - self.target)
                                * (self.cur_temp - self.target))
        for dev in self._devices:
            values = flatten([compass_to_rgb(self.angle)] * dev.num_leds)
            dev.set_lighting(values=values)

    def __str__(self) -> str:
        return f'temperature lighting'


class ThermaltakeLightingEffect(LightingEffect):
    def __init__(self, config):
        super().__init__(config)
        conf_speed = self._config.get('speed', 'normal')
        self._speed = getattr(RGB.Speed, conf_speed.upper())

    def start(self):
        raise NotImplementedError


class FullLightingEffect(ThermaltakeLightingEffect):
    """
    ::: settings: [r, g, b]
    """
    model = 'full'

    def start(self):
        values = []
        try:
            g, r, b = self._config['g'], self._config['r'], self._config['b']
            for i in range(12):
                values.extend([g, r, b])
        except KeyError as e:
            LOGGER.warn('%s not found in config item: lighting_controller', e)

        for device in self._devices:
            device.set_lighting(mode=RGB.Mode.FULL, speed=0x00, values=values)


class PerLEDLightingEffect(ThermaltakeLightingEffect):
    # TODO: per-led config
    # TODO: design a neat way to set this up via config (surely theres a better way then a massive array)
    model = 'perLed'

    def start(self):
        raise NotImplementedError


class FlowLightingEffect(ThermaltakeLightingEffect):
    """
    ::: settings: [speed]
    """
    model = 'flow'

    def start(self):
        for device in self._devices:
            device.set_lighting(mode=RGB.Mode.FLOW, speed=self._speed)


class SpectrumLightingEffect(ThermaltakeLightingEffect):
    """
    ::: settings: [speed]
    """
    model = 'spectrum'

    def start(self):
        for device in self._devices:
            device.set_lighting(mode=RGB.Mode.SPECTRUM, speed=self._speed)


class RippleLightingEffect(ThermaltakeLightingEffect):
    """
    ::: settings: [speed, r, g, b]
    """
    model = 'ripple'

    def start(self):
        try:
            g, r, b = self._config['g'], self._config['r'], self._config['b']
        except KeyError as e:
            LOGGER.warn('%s not found in config item: lighting_controller', e)
            return

        for device in self._devices:
            device.set_lighting(mode=RGB.Mode.RIPPLE, speed=self._speed, values=[g, r, b])


class BlinkLightingEffect(ThermaltakeLightingEffect):
    # TODO: per-led config
    # TODO: design a neat way to set this up via config (surely theres a better way then a massive array)
    """
    ::: settings: [speed, r, g, b]
    """
    model = 'blink'

    def start(self):
        try:
            g, r, b = self._config['g'], self._config['r'], self._config['b']
        except KeyError as e:
            LOGGER.warn('%s not found in config item: lighting_controller', e)
            return

        for device in self._devices:
            values = []
            for i in range(12):
                values.extend([g, r, b])
            device.set_lighting(mode=RGB.Mode.BLINK, speed=self._speed, values=values)


class PulseLightingEffect(ThermaltakeLightingEffect):
    # TODO: per-led config
    # TODO: design a neat way to set this up via config (surely theres a better way then a massive array)
    """
    ::: settings: [speed, r, g, b]
    """
    model = 'pulse'

    def start(self):
        try:
            g, r, b = self._config['g'], self._config['r'], self._config['b']
        except KeyError as e:
            LOGGER.warn('%s not found in config item: lighting_controller', e)
            return

        for device in self._devices:
            values = []
            for i in range(12):
                values.extend([g, r, b])
            device.set_lighting(mode=RGB.Mode.PULSE, speed=self._speed, values=values)


class WaveLightingEffect(ThermaltakeLightingEffect):
    # TODO: per-led config
    # TODO: design a neat way to set this up via config (surely theres a better way then a massive array)
    # 14=wave    requires values (spinning per led)
    model = 'wave'

    def start(self):
        raise NotImplementedError
