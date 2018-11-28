from linux_thermaltake_rgb import devices
from linux_thermaltake_rgb.devices import fans, pumps, lights


def device_factory(controller, port: int, dev_str: str) -> devices.ThermaltakeDevice:
    dev = None
    if dev_str == devices.RIING_PLUS:
        dev = fans.ThermaltakeRiingPlusFan(controller, port)
    elif dev_str == devices.FLOE_RIING_RGB:
        dev = pumps.ThermaltakeRiingPlusFloeRGB(controller, port)
    elif dev_str == devices.PR22D5_PLUS:
        dev = lights.ThermaltakePR22D5Res(controller, port)
    elif dev_str == devices.W4_PLUS:
        dev = lights.ThermaltakeW4PlusWB(controller, port)
    elif dev_str == devices.VGTX_1080_PLUS:
        dev = lights.ThermaltakeVGTX1080PlusWB(controller, port)
    elif dev_str == devices.RAD_PLUS:
        dev = lights.ThermaltakeRadPlusLED(controller, port)
    elif dev_str == devices.LUMI_PLUS:
        dev = lights.ThermaltakeLumiPlusLED(controller, port)

    controller.attach_device(port, dev)
    return dev
