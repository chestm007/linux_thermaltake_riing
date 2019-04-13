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
import os

import yaml
from mock import patch

from base_test_object import BaseTestObject
from linux_thermaltake_rgb.controllers import ThermaltakeController
from linux_thermaltake_rgb.daemon.config import Config
from linux_thermaltake_rgb.devices import ThermaltakeDevice
from linux_thermaltake_rgb.devices.psus import ThermaltakePSUDevice


class ConfigTest(BaseTestObject):
    @patch('linux_thermaltake_rgb.drivers.ThermaltakeControllerDriver._initialize_device', autospec=True)
    def test_load_from_assets(self, init_dev):
        def verify_config(config):
            for thing in (config, config.controllers, config.fan_manager, config.lighting_manager):
                self.assertIsNotNone(thing)

        # verify absolute load codepath is good
        Config.abs_config_dir = str(Config.rel_config_dir)
        verify_config(Config())

        # verify relative load codepath is good
        Config.rel_config_dir = Config.abs_config_dir
        del Config.abs_config_dir
        Config.abs_config_dir = ''
        verify_config(Config())

    def load_config_from_string(self, config):
        class MockConfig(Config):
            def load_config(self):
                return yaml.load(config)
        return MockConfig()

    def load_g3_config(self):
        return self.load_config_from_string(G3_CONFIG)

    @patch('linux_thermaltake_rgb.drivers.ThermaltakeControllerDriver._initialize_device', autospec=True)
    def test_g3_config(self, init_dev):
        config = self.load_g3_config()
        self.assertEqual(len(config.controllers), 5, 'not all controllers recognized in config')
        for controller in config.controllers:
            self.assertEqual(controller.get('type'), 'g3')
            self.assertIn('unit', controller)

            ThermaltakeController.factory(controller.get('type'))
            self.assertTrue(init_dev.called)

    def load_irgbplus_config(self):
        return self.load_config_from_string(IRGBPLUS_CONFIG)

    @patch('linux_thermaltake_rgb.drivers.ThermaltakeControllerDriver._initialize_device', autospec=True)
    def test_irgbplus_config(self, init_dev):

        config = self.load_irgbplus_config()
        for psu in config.psus:
            self.assertEqual(psu.get('type'), 'irgbplus')

            dev = ThermaltakeDevice.factory(psu.get('type'))
            self.assertIsInstance(dev, ThermaltakePSUDevice)
            self.assertTrue(init_dev.called)

    @patch('linux_thermaltake_rgb.drivers.ThermaltakeControllerDriver._initialize_device', autospec=True)
    def test_full_config(self, init_dev):
        config = self.load_config_from_string(G3_CONFIG + IRGBPLUS_CONFIG)
        self.assertIsNotNone(config.controllers)
        self.assertIsNotNone(config.psus)

        self.assertEqual(config.psus[0]['type'], 'irgbplus')


IRGBPLUS_CONFIG = """
psus:
  - type: irgbplus
"""

G3_CONFIG = """
controllers:
  - unit: 1
    type: g3
    devices:
      1: Riing Plus
      2: Riing Plus
      3: Riing Plus
      4: Riing Plus
      5: Floe Riing RGB
  - unit: 2
    type: g3
    devices:
      1: Riing Plus
      2: Riing Plus
      3: Riing Plus
      4: Pacific V-GTX 1080Ti Plus GPU Waterblock
      5: Pacific W4 Plus CPU Waterblock
  - unit: 3
    type: g3
    devices:
      1: Riing Plus
      2: Riing Plus
      3: Riing Plus
      4: Pacific V-GTX 1080Ti Plus GPU Waterblock
      5: Pacific PR22-D5 Plus
  - unit: 4
    type: g3
    devices:
      1: Riing Plus
      2: Riing Plus
      3: Riing Plus
      4: Pacific V-GTX 1080Ti Plus GPU Waterblock
      5: Lumi Plus LED Strip
  - unit: 5
    type: g3
    devices:
      1: Riing Plus
      2: Riing Plus
      3: Riing Plus
      4: Riing Plus
      5: Lumi Plus LED Strip
"""
