from threading import Thread

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject

from linux_thermaltake_rgb.fan_manager import FanModel
from linux_thermaltake_rgb.lighting_manager import LightingEffect

DBusGMainLoop(set_as_default=True)

OPATH = "/org/thermaltake/Daemon"
IFACE = "org.thermaltake.Daemon"
BUS_NAME = "org.thermaltake.Daemon"


class ThermaltakeDbusService(dbus.service.Object):
    def __init__(self, daemon):
        self.daemon = daemon
        bus = dbus.SessionBus()
        bus.request_name(BUS_NAME)
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, OPATH)
        self.thread = None

    @dbus.service.method(dbus_interface=IFACE, in_signature="", out_signature="s")
    def set_fan_controller(self, *args):
        if len(args) > 0:
            if args[0] in ('locked_speed', 'temp_target'):
                fc = FanModel.factory(*args)
                self.daemon.fan_manager.set_model(fc)
                return "success"
        return "argument 0 must be in [locked_speed|temp_target]"

    @dbus.service.method(dbus_interface=IFACE, in_signature="", out_signature="s")
    def set_lighting_controller(self, *args):
        if len(args) > 0:
            if args[0] in ('static', 'alternating', 'rgb_spectrum',
                           'spinning_rgb_spectrum', 'temperature'):
                fc = LightingEffect.factory(*args)
                self.daemon.lighting_manager.set_model(fc)
                return "success"
        return "argument 0 must be in [static|alternating|rgb_spectrum]"

    @dbus.service.method(dbus_interface=IFACE, in_signature="", out_signature="s")
    def set_lighting_brightness(self, *args):
        if len(args) > 0:
            self.daemon.lighting_manager.set_brightness(args[0])
            return "success"

    @dbus.service.method(dbus_interface=IFACE, in_signature="", out_signature="s")
    def set_lighting_msec(self, *args):
        if len(args) > 0:
            self.daemon.lighting_manager.set_light_update_msec(args[0])
            return "success"

    def start(self):
        self.thread = Thread(target=self._main_loop)
        self.thread.start()

    def stop(self):
        self.loop.stop()

    def _main_loop(self):
        self.loop = GObject.MainLoop()
        self.loop.run()


if __name__ == "__main__":
    a = ThermaltakeDbusService()
    loop = GObject.MainLoop()
    loop.run()
