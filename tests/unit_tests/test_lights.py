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
from base_test_object import BaseTestObject
from linux_thermaltake_rgb.lighting_manager import LightingEffect


class LightTest(BaseTestObject):

    def test_light_factory(self):
        config = {
            'odd_rgb': dict(r=4, g=4, b=4),
            'even_rgb': dict(r=4, g=4, b=4)
        }
        for clazz in LightingEffect.inheritors():
            if clazz.model is None:
                continue
            config['model'] = clazz.model

            effect = LightingEffect.factory(config)
            self.assertIsInstance(effect, LightingEffect)
