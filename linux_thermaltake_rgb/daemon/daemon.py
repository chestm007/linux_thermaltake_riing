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

from linux_thermaltake_rgb.daemon.config import Config
from linux_thermaltake_rgb.daemon.dbus_service.service import ThermaltakeDbusService
from linux_thermaltake_rgb.daemon.devices import ThermaltakeFanDevice, ThermaltakeRGBDevice
from linux_thermaltake_rgb.daemon.devices.factory import device_factory
from linux_thermaltake_rgb.daemon.fan_manager import FanManager, fan_controller_factory
from linux_thermaltake_rgb.daemon.lighting_manager import LightingManager, lighting_controller_factory
from linux_thermaltake_rgb.driver.driver import ThermaltakeRiingPlusDriver


class ThermaltakeDaemon:
    def __init__(self):
        self.config = Config()

        fan_controller = fan_controller_factory(**self.config.fan_controller)
        self.fan_manager = FanManager(fan_controller)

        lighting_controller = lighting_controller_factory(**self.config.lighting_controller)
        self.lighting_manager = LightingManager(lighting_controller)

        self.dbus_service = ThermaltakeDbusService(self)

        self.driver = ThermaltakeRiingPlusDriver()
        self._thread = Thread(target=self._main_loop)
        self.attached_devices = {}
        self._continue = False
        for id, _type in self.config.devices.items():
            self.register_attached_device(id, _type)

    def register_attached_device(self, id: int, _type: str):
        dev = device_factory(self.driver, int(id), _type)
        if isinstance(dev, ThermaltakeFanDevice):
            self.fan_manager.attach_device(dev)
        if isinstance(dev, ThermaltakeRGBDevice):
            self.lighting_manager.attach_device(dev)
        self.attached_devices[id] = device_factory(self.driver, int(id), _type)

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
