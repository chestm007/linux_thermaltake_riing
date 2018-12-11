from linux_thermaltake_rgb import drivers


class ThermaltakeG3Controller:
    def __init__(self, unit=1):
        self.unit = unit
        self.devices = {}
        self.ports = 5
        self.driver = drivers.ThermaltakeG3ControllerDriver(unit)

    def attach_device(self, port=None, dev=None):
        self.devices[port] = dev
        return self.devices[port]

    def save_profile(self):
        self.driver.save_profile()


def controller_factory(unit_type=None, unit=1, **kwargs) -> ThermaltakeG3Controller:
    if unit_type == 'g3':
        return ThermaltakeG3Controller(unit)
