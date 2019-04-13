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

from linux_thermaltake_rgb import LOGGER


class Config:
    abs_config_dir = '/etc/linux_thermaltake_rgb'
    rel_config_dir = 'linux_thermaltake_rgb/assets'
    config_file_name = 'config.yml'

    def __init__(self):
        self.controllers = None
        self.fan_manager = None
        self.lighting_manager = None
        self.psus = None

        # if we have config in /etc, use it, otherwise try and use repository config file
        if os.path.isdir(self.abs_config_dir):
            if os.path.isfile(os.path.join(self.abs_config_dir, self.config_file_name)):
                self.config_dir = self.abs_config_dir
        elif os.path.isdir(self.rel_config_dir):
            if os.path.isfile(os.path.join(self.rel_config_dir, self.config_file_name)):
                self.config_dir = self.rel_config_dir
        else:
            raise Exception('no config file found')

        config = self.load_config()
        self.parse_config(config)

    def load_config(self):
        with open('{}/{}'.format(self.config_dir, self.config_file_name)) as cfg:
            cfg_str = cfg.readlines()
        cfg_lines = []
        for s in cfg_str:
            # remove comments and blank lines
            if not s.strip().startswith('#') and len(s) > 1:
                cfg_lines.append(s)

        cfg = ''.join(cfg_lines)
        LOGGER.debug('raw config file\n** start **\n\n%s\n** end **\n', cfg)
        return yaml.load(cfg)

    def parse_config(self, config):
            self.controllers = config.get('controllers')
            LOGGER.debug(config.get('controllers'))
            # self.devices = config.get('devices')
            LOGGER.debug(config.get('fan_manager'))
            self.fan_manager = config.get('fan_manager')
            LOGGER.debug(config.get('lighting_manager'))
            self.lighting_manager = config.get('lighting_manager')
            LOGGER.debug(config.get('psus'))
            self.psus = config.get('psus')
