import time
from threading import Thread


def lighting_controller_factory(**kwargs):
    args = dict(kwargs)
    _type = args.pop('type')
    if _type == 'static':
        return StaticLightingController(**args)


class LightingController:
    def main(self, device):
        """
        returns a hex array to set the lights too
        """
        raise NotImplementedError


class StaticLightingController(LightingController):
    def __init__(self, r: int, g: int, b: int):
        self.r, self.g, self.b = r, g, b

    def main(self, device) -> list:
        data = []
        if device.index_per_led == 3:
            for i in range(device.num_leds):
                data.extend([self.g, self.r, self.b])
        return data


class LightingManager:
    def __init__(self, initial_controller: LightingController=None):
        self._continue = False
        self._thread = Thread(target=self._main_loop)
        self._devices = []
        self._controller = initial_controller

    def attach_device(self, device):
        self._devices.append(device)

    def _main_loop(self):
        while self._continue:
            for dev in self._devices:
                lights = self._controller.main(dev)
                dev.set_lighting(lights)
            time.sleep(0.05)

    def start(self):
        self._continue = True
        if self._controller is None:
            self._controller = LightingController()
        self._thread.start()

    def stop(self):
        self._continue = False
        self._thread.join()
