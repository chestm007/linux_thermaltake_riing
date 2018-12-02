import os

from base_test_object import BaseTestObject
from linux_thermaltake_rgb.daemon.config import Config


class ConfigTest(BaseTestObject):
    def test_load_from_assets(self):
        def verify_config(config):
            for thing in (config, config.controllers, config.fan_manager, config.lighting_manager):
                self.assertIsNotNone(thing)

        # verify absolute load codepath is good
        Config.abs_config_dir = os.path.join('..', Config.rel_config_dir)
        verify_config(Config())

        # verify relative load codepath is good
        Config.rel_config_dir = Config.abs_config_dir
        del Config.abs_config_dir
        Config.abs_config_dir = ''
        verify_config(Config())

