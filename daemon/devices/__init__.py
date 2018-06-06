from globals.protocol_definitions import PROTOCOL_SET, PROTOCOL_LIGHT, PROTOCOL_FAN, PROTOCOL_GET


class ThermaltakeDevice:

    def __init__(self, driver, id: int):
        self.id = int(id)
        self.driver = driver


class ThermaltakeRGBDevice(ThermaltakeDevice):
    num_leds = 0
    index_per_led = 0

    def set_lighting(self, values: list) -> None:
        """
        for the sake of performance this will assume the data your passing in is correct.
        if it isnt the worst that will happen (i guess) is the lights wont show up as
        expected.
        :param values: [r,g,b...]
        """
        data = [PROTOCOL_SET, PROTOCOL_LIGHT, self.id, 0x18]
        data.extend(values)
        self.driver.write_out(data)


class ThermaltakeFanDevice(ThermaltakeDevice):
    def set_fan_speed(self, speed: int):
        data = [PROTOCOL_SET, PROTOCOL_FAN, self.id, 0x01, int(speed)]
        self.driver.write_out(data)

    def get_fan_speed(self):
        data = [PROTOCOL_GET, PROTOCOL_FAN, self.id]
        self.driver.write_out(data)
        self.driver.read_in()


