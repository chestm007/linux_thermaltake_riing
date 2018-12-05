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

from linux_thermaltake_rgb import LOGGER
from linux_thermaltake_rgb.controllers import controller_factory
from linux_thermaltake_rgb.fan_manager import FanModel
from linux_thermaltake_rgb.daemon.config import Config
from linux_thermaltake_rgb.daemon.dbus_service.service import ThermaltakeDbusService
from linux_thermaltake_rgb.lighting_manager import LightingEffect
from linux_thermaltake_rgb import devices
from linux_thermaltake_rgb.fan_manager import FanManager
from linux_thermaltake_rgb.devices import ThermaltakeDevice


class ThermaltakeDaemon:
    def __init__(self):
        self.config = Config()

        fan_model = FanModel.factory(self.config.fan_manager)
        self.fan_manager = FanManager(fan_model)

        self.lighting_manager = LightingEffect.factory(self.config.lighting_manager)

        self.dbus_service = ThermaltakeDbusService(self)

        self.attached_devices = {}
        self.controllers = {}

        for controller in self.config.controllers:
            self.controllers[controller['unit']] = controller_factory(controller['type'], controller['unit'])
            for id, model in controller['devices'].items():
                dev = ThermaltakeDevice.factory(model, self.controllers[controller['unit']], id)
                self.controllers[controller['unit']].attach_device(id, dev)
                self.register_attached_device(controller['unit'], id, dev)

        self._thread = Thread(target=self._main_loop)

        self._continue = False

    def register_attached_device(self, unit, port, dev=None):
        if isinstance(dev, devices.ThermaltakeFanDevice):
            self.fan_manager.attach_device(dev)
        if isinstance(dev, devices.ThermaltakeRGBDevice):
            self.lighting_manager.attach_device(dev)

        self.attached_devices[f'{unit}:{port}'] = dev

    def run(self):
        self._continue = True
        self._thread.start()
        self.lighting_manager.start()
        self.fan_manager.start()
        self.dbus_service.start()

    def stop(self):
        self._continue = False
        self.lighting_manager.stop()
        self.fan_manager.stop()
        self._thread.join()
        self.dbus_service.stop()

    def _main_loop(self):
        while self._continue:
            time.sleep(1)
