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

from linux_thermaltake_rgb.controllers import ThermaltakeController
from linux_thermaltake_rgb.fan_manager import FanModel
from linux_thermaltake_rgb.daemon.config import Config
from linux_thermaltake_rgb.lighting_manager import LightingEffect
from linux_thermaltake_rgb import devices, LOGGER
from linux_thermaltake_rgb.fan_manager import FanManager
from linux_thermaltake_rgb.devices import ThermaltakeDevice


class ThermaltakeDaemon:
    def __init__(self):
        LOGGER.info('initializing thermaltake rgb daemon')

        LOGGER.debug('loading config')
        self.config = Config()

        LOGGER.debug('creating fan manager')
        fan_model = FanModel.factory(self.config.fan_manager)
        self.fan_manager = FanManager(fan_model)

        LOGGER.debug('creating lighting manager')
        self.lighting_manager = LightingEffect.factory(self.config.lighting_manager)

        self.attached_devices = {}
        self.controllers = {}

        LOGGER.debug('configuring controllers')
        for controller in self.config.controllers:
            self.controllers[controller['unit']] = ThermaltakeController.factory(controller['type'], controller.get('unit'))
            for id, model in controller['devices'].items():
                LOGGER.debug(' configuring devices for controller %s: %s', controller['type'], controller.get('unit'))
                dev = ThermaltakeDevice.factory(model, self.controllers[controller['unit']], id)
                self.controllers[controller['unit']].attach_device(id, dev)
                self.register_attached_device(controller['unit'], id, dev)
        self.psus = []

        if self.config.psus is not None:
            LOGGER.debug('configuring PSUs')
            for i, psu in enumerate(self.config.psus):
                LOGGER.debug('configuring PSU %s', psu.get('type'))
                dev = ThermaltakeDevice.factory(psu.get('type'))
                self.psus.append(dev)
                self.register_attached_device('psu', i, dev)

        self._thread = Thread(target=self._main_loop)
        self._continue = False

    def register_attached_device(self, unit, port, dev=None):
        if isinstance(dev, devices.ThermaltakeFanDevice):
            LOGGER.debug('  registering %s with fan manager', dev.model)
            self.fan_manager.attach_device(dev)
        if isinstance(dev, devices.ThermaltakeRGBDevice):
            LOGGER.debug('  registering %s with lighting manager', dev.model)
            self.lighting_manager.attach_device(dev)

        self.attached_devices[f'{unit}:{port}'] = dev

    def run(self):
        self._continue = True
        LOGGER.debug('starting main thread')
        self._thread.start()
        LOGGER.debug('starting lighting manager')
        self.lighting_manager.start()
        LOGGER.debug('starting fan manager')
        self.fan_manager.start()

    def stop(self):
        LOGGER.debug('recieved exit command')
        self._continue = False
        LOGGER.debug('stopping lighting manager')
        self.lighting_manager.stop()
        LOGGER.debug('stopping fan manager')
        self.fan_manager.stop()
        LOGGER.debug('stopping main thread')
        self._thread.join()
        LOGGER.debug('saving controller profiles')
        for controller in self.controllers.values():
            controller.save_profile()

    def _main_loop(self):
        while self._continue:
            time.sleep(1)
