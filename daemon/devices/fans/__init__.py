from daemon.devices import ThermaltakeRGBDevice, ThermaltakeFanDevice


class ThermaltakeRiingPlusFan(ThermaltakeRGBDevice, ThermaltakeFanDevice):
    num_leds = 12
    index_per_led = 3
