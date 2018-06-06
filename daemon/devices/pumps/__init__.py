from daemon.devices import ThermaltakeRGBDevice


class ThermaltakeRiingPlusFloeRGB(ThermaltakeRGBDevice):
    num_leds = 6
    index_per_led = 6