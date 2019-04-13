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
import sys

import logging
from io import StringIO

from mock import patch
from base_test_object import BaseTestObject
from linux_thermaltake_rgb import LOGGER
from linux_thermaltake_rgb.daemon.daemon import ThermaltakeDaemon, Config
from linux_thermaltake_rgb.devices.psus import ThermaltakePSUDevice


class DaemonMockIntegrationTest(BaseTestObject):
    def setUp(self):
        self.config_abs_path = str(Config.abs_config_dir)
        Config.abs_config_dir = ''

    @patch('linux_thermaltake_rgb.drivers.ThermaltakeControllerDriver._initialize_device', autospec=True)
    def test_basic_startup(self, init_dev):
        LOGGER.setLevel(logging.DEBUG)
        stream = StringIO()
        stream_handler = logging.StreamHandler(stream)
        # stream_handler = logging.StreamHandler(sys.stdout)

        LOGGER.addHandler(stream_handler)
        try:
            daemon = ThermaltakeDaemon()
        finally:
            stream_handler.flush()
            LOGGER.removeHandler(stream_handler)
        self.assertIsNotNone(daemon)
        self.assertIsNotNone(daemon.config.controllers)
        self.assertTrue(init_dev.called)
        for psu in daemon.psus:
            self.assertIsInstance(psu, ThermaltakePSUDevice)

        logging_output = stream.getvalue()
        print(logging_output)
        for keyword in ('ThermaltakePSUDevice', '** start **', '** end **'):
            self.assertIn(keyword, logging_output)

    def tearDown(self):
        Config.abs_config_dir = str(self.config_abs_path)
