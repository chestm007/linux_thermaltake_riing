from linux_thermaltake_rgb import drivers


class ThermaltakeController:
    def __init__(self, unit=1):
        self.unit = unit
        self.devices = {}
        self.ports = 5
        self.driver = None
        self.init()
        if self.driver is None:
            raise RuntimeError('driver not set')

    def init(self):
        pass

    def attach_device(self, port=None, dev=None):
        self.devices[port] = dev
        return self.devices[port]

    def save_profile(self):
        self.driver.save_profile()


class ThermaltakeG3Controller(ThermaltakeController):
    def init(self):
        self.driver = drivers.ThermaltakeG3ControllerDriver(self.unit)


class ThermaltakeRiingTrioController(ThermaltakeController):
    def init(self):
        self.driver = drivers.ThermaltakeRiingTrioControllerDriver(self.unit)


def controller_factory(unit_type=None, unit=1, **kwargs) -> ThermaltakeController:
    if unit_type.lower() == 'g3':
        return ThermaltakeG3Controller(unit)
    
    elif unit_type.lower() == 'riingtrio':
        return ThermaltakeRiingTrioController(unit)
