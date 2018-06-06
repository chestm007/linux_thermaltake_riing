import os

import yaml


class Config:

    def __init__(self):
        if not os.path.isdir('/etc/thermaltake_riing'):
            os.mkdir('/etc/thermaltake_riing')

        with open('/etc/thermaltake_riing/daemon_config.yml') as cfg:
            config = yaml.load(cfg)
            self.devices = config.get('devices')
            self.fan_controller = config.get('fan_controller')
            self.lighting_controller = config.get('lighting_controller')

