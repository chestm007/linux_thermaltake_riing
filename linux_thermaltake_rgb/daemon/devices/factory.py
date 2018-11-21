"""
linux_thermaltake_rgb
Software to control your thermaltake hardware
Copyright (C) 2018  Max Chesterfield (chestm007@hotmail.com)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from linux_thermaltake_rgb.daemon.devices import ThermaltakeDevice
from linux_thermaltake_rgb.daemon.devices.fans import ThermaltakeRiingPlusFan
from linux_thermaltake_rgb.daemon.devices.pumps import ThermaltakeRiingPlusFloeRGB
from linux_thermaltake_rgb.globals.device_definitions import RIING_PLUS, FLOE_RIING_RGB


def device_factory(daemon, id: int, _type: str) -> ThermaltakeDevice:
    if _type == RIING_PLUS:
        return ThermaltakeRiingPlusFan(daemon, id)
    elif _type == FLOE_RIING_RGB:
        return ThermaltakeRiingPlusFloeRGB(daemon, id)
