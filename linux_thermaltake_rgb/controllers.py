from linux_thermaltake_rgb import drivers


class ThermaltakeController:
    def __init__(self, unit=None):
        self.unit = unit
        self.devices = {}
        self.ports = 0

    def attach_device(self, port=None, dev=None):
        self.devices[port] = dev
        return self.devices[port]


class ThermaltakeG3Controller(ThermaltakeController):
    def __init__(self, unit=1, **kwargs):
        ThermaltakeController.__init__(self, unit)
        self.ports = 5
        self.driver = drivers.ThermaltakeG3ControllerDriver(unit)


def controller_factory(unit_type=None, unit=1, **kwargs) -> ThermaltakeController:
    if unit_type == 'g3':
        return ThermaltakeG3Controller(unit, **kwargs)
