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
from base_test_object import BaseTestObject


class ControllerTest(BaseTestObject):

    @patch('linux_thermaltake_rgb.drivers.ThermaltakeControllerDriver._initialize_device', autospec=True)
    def test_controller_factory(self, init_dev):
        for type_ in ('g3', ):
            for case_variant in (str.lower, str.upper, str):
                self.assertIsInstance(ThermaltakeController.factory(case_variant(type_)),
                                      ThermaltakeController,
                                      '{} not recognized'.format(type_))
                self.assertTrue(init_dev.called, '{} did not initialize the driver'.format(type_))
