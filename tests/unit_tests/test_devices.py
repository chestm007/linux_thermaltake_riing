from linux_thermaltake_rgb.controllers import controller_factory
from linux_thermaltake_rgb.devices import ThermaltakeDevice
from base_test_object import BaseTestObject


class DeviceTest(BaseTestObject):

    def test_device_factory(self):
        controller = controller_factory('g3')
        for i, clazz in enumerate(ThermaltakeDevice.inheritors()):
            if clazz.model is None:
                continue

            dev = ThermaltakeDevice.factory(clazz.model, controller, 1)
            controller.attach_device(i, dev)
            self.assertIsInstance(ThermaltakeDevice.factory(clazz.model, controller, 1), clazz)
