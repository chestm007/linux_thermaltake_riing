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
from mock import patch

from linux_thermaltake_rgb.controllers import ThermaltakeController
from linux_thermaltake_rgb.devices import ThermaltakeDevice
from base_test_object import BaseTestObject


class DeviceTest(BaseTestObject):

    @patch('linux_thermaltake_rgb.drivers.ThermaltakeControllerDriver._initialize_device', autospec=True)
    def test_device_factory(self, init_dev):
        controller = ThermaltakeController.factory('g3')
        for i, clazz in enumerate(ThermaltakeDevice.inheritors()):
            if clazz.model is None:
                continue

            dev = ThermaltakeDevice.factory(clazz.model, controller, 1)
            controller.attach_device(i, dev)
            self.assertIsInstance(ThermaltakeDevice.factory(clazz.model, controller, 1), clazz)
            self.assertTrue(init_dev.called)
