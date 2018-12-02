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

import usb


class ThermaltakeG3ControllerDriver:
    VENDOR_ID = 0x264a
    PRODUCT_ID_BASE = 0x1fa5

    def __init__(self, unit=1):
        self.vendor_id = self.VENDOR_ID
        self.product_id = self.PRODUCT_ID_BASE + (unit - 1)

        self._initialize_device()

    def _initialize_device(self):
        self.device = usb.core.find(idVendor=self.vendor_id,
                                    idProduct=self.product_id)
        # fail safe incase last device usage was dirty
        self.device.reset()

        if self.device is None:
            raise ValueError('Device not found')

        # Linux kernel sets up a device driver for USB device, which you have
        # to detach. Otherwise trying to interact with the device gives a
        # 'Resource Busy' error.
        try:
            self.device.detach_kernel_driver(0)
        except Exception as e:
            pass  # already unregistered

        self.device.set_configuration()

        # claim the device
        try:
            usb.util.claim_interface(self.device, 0)
        except usb.core.USBError as e:
            raise

        self.cfg = self.device.get_active_configuration()
        self.interface = self.cfg[(0, 0)]
        self.endpoint_out = usb.util.find_descriptor(
            self.interface,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        assert self.endpoint_out is not None

        self.endpoint_in = usb.util.find_descriptor(
            self.interface,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
        assert self.endpoint_in is not None

        # initialize/reset the device
        self.init_controller()

    @staticmethod
    def _generate_data_array(length: int = 64, value: int = 0x00) -> list:
        """
        helper function to generate a zeroed out array of length size
        """
        return [value for i in range(length)]

    def _populate_partial_data_array(self, in_array: list, length=64) -> list:
        """
        helper function to fill the rest of the array with 0x00
        until desired length is attained
        """
        array = list(in_array)
        array.extend(
            self._generate_data_array(length - len(in_array))
        )
        return array

    def write_out(self, data: list, length: int = 64) -> None:
        try:
            self.endpoint_out.write(self._populate_partial_data_array(data, length))
        except OverflowError:
            return

    def read_out(self, length: int = 64) -> bytearray:
        return self.endpoint_out.read(length)

    def write_in(self, data: list, length: int = 64) -> None:
        self.endpoint_in.write(self._populate_partial_data_array(data, length))

    def read_in(self, length: int = 64) -> bytearray:
        return self.endpoint_in.read(length)

    def init_controller(self):
        self.write_out([0xfe, 0x33])

    def save_profile(self):
        self.write_out([0x32, 0x53])
