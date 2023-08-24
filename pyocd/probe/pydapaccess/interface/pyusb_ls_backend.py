# pyOCD debugger
# Copyright (c) 2019-2021 Arm Limited
# Copyright (c) 2021 mentha
# Copyright (c) 2021-2022 Chris Reed
# Copyright (c) 2023 Michael Sparmann
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import errno
import platform
import time

from .interface import Interface
from .common import (
    USB_CLASS_VENDOR_SPECIFIC,
    filter_device_by_class,
    is_known_cmsis_dap_vid_pid,
    generate_device_unique_id,
    )
from ..dap_access_api import DAPAccessIntf
from ... import common
from ....utility.timeout import Timeout

LOG = logging.getLogger(__name__)
TRACE = LOG.getChild("trace")
TRACE.setLevel(logging.CRITICAL)

try:
    import libusb_package
    import usb.core
    import usb.util
except ImportError:
    IS_AVAILABLE = False
else:
    IS_AVAILABLE = True

class PyUSBLS(Interface):
    """@brief CMSIS-DAP Low Speed interface using pyUSB."""

    isAvailable = IS_AVAILABLE

    def __init__(self, dev):
        super().__init__()
        self.vid = dev.idVendor
        self.pid = dev.idProduct
        self.product_name = dev.product or f"{dev.idProduct:#06x}"
        self.vendor_name = dev.manufacturer or f"{dev.idVendor:#06x}"
        self.serial_number = dev.serial_number \
                or generate_device_unique_id(dev.idProduct, dev.idVendor, dev.bus, dev.address)
        self.dev = None
        self.intf_number = None
        self.kernel_driver_was_attached = False
        self.closed = True
        self.packet_size = 64
        self.depth = 0

    def open(self):
        assert self.closed is True

        # Get device handle
        dev = libusb_package.find(custom_match=HasCmsisDapLSInterface(self.serial_number))
        if dev is None:
            raise DAPAccessIntf.DeviceError("Device %s not found" %
                                            self.serial_number)

        # get active config
        config = dev.get_active_configuration()

        # Get CMSIS-DAP Low Speed interface
        interface = usb.util.find_descriptor(config, custom_match=_match_cmsis_dap_ls_interface)
        if interface is None:
            raise DAPAccessIntf.DeviceError("Device %s has no CMSIS-DAP Low Speed interface" %
                                            self.serial_number)
        interface_number = interface.bInterfaceNumber

        # Explicitly claim the interface
        try:
            usb.util.claim_interface(dev, interface_number)
        except usb.core.USBError as exc:
            raise DAPAccessIntf.DeviceError("Unable to open device") from exc

        # Update all class variables if we made it here
        self.dev = dev
        self.intf_number = interface_number
        self.closed = False

    @staticmethod
    def get_all_connected_interfaces():
        """@brief Returns all the connected devices with a CMSIS-DAP Low Speed interface."""
        # find all cmsis-dap devices
        try:
            all_devices = libusb_package.find(find_all=True, custom_match=HasCmsisDapLSInterface())
        except usb.core.NoBackendError:
            common.show_no_libusb_warning()
            return []

        # iterate on all devices found
        boards = []
        for board in all_devices:
            new_board = PyUSBLS(board)
            boards.append(new_board)

        return boards

    def write(self, data):
        """@brief Write data to the interface."""

        if TRACE.isEnabledFor(logging.DEBUG):
            TRACE.debug("  USB OUT> (%d) %s", len(data), ' '.join([f'{i:02x}' for i in data]))

        self.dev.ctrl_transfer(0x21, 0x09, 0x200, self.intf_number, data, timeout=self.DEFAULT_USB_TIMEOUT_MS)
        self.depth += 1

    def read(self):
        """@brief Read data from the interface."""
        self.depth -= 1
        if not self.depth: time.sleep(0.0001)
        data = self.dev.ctrl_transfer(0xa1, 0x01, 0x100, self.intf_number, 64, timeout=self.DEFAULT_USB_TIMEOUT_MS)
        return data

    def close(self):
        """@brief Close the USB interface."""
        assert self.closed is False

        self.closed = True
        usb.util.release_interface(self.dev, self.intf_number)
        usb.util.dispose_resources(self.dev)
        self.dev = None
        self.intf_number = None

def _match_cmsis_dap_ls_interface(interface):
    """@brief Returns true for a CMSIS-DAP LS interface.

    This match function performs several tests on the provided USB interface descriptor, to
    determine whether it is a CMSIS-DAP Low Speed interface. These requirements must be met by the
    interface:

    1. Have an interface name string containing "CMSIS-DAP".
    2. bInterfaceClass must be 0xff.
    3. bInterfaceSubClass must be 0x7c.
    4. bInterfaceProtocol must be 0xd0.
    """
    interface_name = usb.util.get_string(interface.device, interface.iInterface)

    # This tells us whether the interface is CMSIS-DAP, but not which variant.
    if (interface_name is None) or ("CMSIS-DAP" not in interface_name):
        return False

    # Now check the interface class to distinguish CMSIS-DAP Low Speed from other variants.
    if (interface.bInterfaceClass != USB_CLASS_VENDOR_SPECIFIC) \
        or (interface.bInterfaceSubClass != 0x7c) \
        or (interface.bInterfaceProtocol != 0xd0):
        return False

    # All checks passed, this is a CMSIS-DAP Low Speed interface!
    return True

class HasCmsisDapLSInterface:
    """@brief CMSIS-DAP Low Speed match class to be used with usb.core.find"""

    def __init__(self, serial=None):
        """@brief Create a new FindDap object with an optional serial number"""
        self._serial = serial

    def __call__(self, dev):
        """@brief Return True if this is a CMSIS-DAP Low Speed device, False otherwise"""
        # Check if the device class is a valid one for CMSIS-DAP.
        if filter_device_by_class(dev.idVendor, dev.idProduct, dev.bDeviceClass):
            return False

        try:
            config = dev.get_active_configuration()
            cmsis_dap_interface = usb.util.find_descriptor(config, custom_match=_match_cmsis_dap_ls_interface)
        except usb.core.USBError as error:
            # Produce a more helpful error message if we get a permissions error on Linux.
            if error.errno == errno.EACCES and platform.system() == "Linux" \
                and common.should_show_libusb_device_error((dev.idVendor, dev.idProduct)):
                msg = ("%s while trying to interrogate a USB device "
                   "(VID=%04x PID=%04x). This can probably be remedied with a udev rule. "
                   "See <https://github.com/pyocd/pyOCD/tree/master/udev> for help." %
                   (error, dev.idVendor, dev.idProduct))
                # If we recognize this device as one that should be CMSIS-DAP, we can raise
                # the level of the log message since it's almost certainly a permissions issue.
                if is_known_cmsis_dap_vid_pid(dev.idVendor, dev.idProduct):
                    LOG.warning(msg)
                else:
                    LOG.debug(msg)
            return False
        except (IndexError, NotImplementedError, ValueError, UnicodeDecodeError) as error:
            return False

        if cmsis_dap_interface is None:
            return False

        if self._serial is not None:
            if dev.serial_number is None:
                if self._serial == "":
                    return True
                if self._serial == generate_device_unique_id(dev.idProduct, dev.idVendor, dev.bus, dev.address):
                    return True
            if self._serial != dev.serial_number:
                return False
        return True
