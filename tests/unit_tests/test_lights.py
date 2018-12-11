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
