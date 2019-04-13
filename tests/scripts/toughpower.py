#! /usr/bin/python3
from linux_thermaltake_rgb.lighting_manager import LightingEffect
from linux_thermaltake_rgb.devices.psus import ThermaltakePSUDevice
import random

lighting_config = dict(
    model='full',
    r=random.randint(1, 200),
    g=random.randint(1, 200),
    b=random.randint(1, 200),
)
lighting = LightingEffect.factory(lighting_config)

psu = ThermaltakePSUDevice()
lighting.attach_device(psu)

lighting.start()

