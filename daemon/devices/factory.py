from daemon.devices import ThermaltakeDevice
from daemon.devices.fans import ThermaltakeRiingPlusFan
from daemon.devices.pumps import ThermaltakeRiingPlusFloeRGB
from globals.device_definitions import RIING_PLUS, FLOE_RIING_RGB


def device_factory(daemon, id: int, _type: str) -> ThermaltakeDevice:
    if _type == RIING_PLUS:
        return ThermaltakeRiingPlusFan(daemon, id)
    elif _type == FLOE_RIING_RGB:
        return ThermaltakeRiingPlusFloeRGB(daemon, id)