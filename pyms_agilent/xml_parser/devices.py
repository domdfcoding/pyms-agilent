#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  devices.py
"""
Parser for Devices.xml
"""
#
#  Copyright © 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import pathlib
from typing import Optional, Sequence

# 3rd party
import importlib_resources
import lxml.objectify
from domdf_python_tools.bases import Dictable
from domdf_python_tools.typing import PathLike

# this package
from pyms_agilent.xml_parser import agilent_xsd

# this package
from .acq_method import tag2dict
from .core import XMLList

__all__ = ["Device", "DeviceList", "read_devices_xml"]


class Device(Dictable):
	"""
	Represents a device parsed from ``Devices.xml``.

	:param device_id: The ID of the device.
	:param display_name: The display name of the device.
	:param driver_version: The version of the device's driver
	:param firmware_version: The version of the device's firmware
	:param model_number: The device's model version
	:param ordinal_number:
	:param serial_number: The serial number of the device.
	:param type_: The type of device
		TODO: Enum
	:param stored_data_type: The type of stored data
		TODO: Enum
	:param delay:
		TODO: Enum
	:param vendor:
		TODO: Enum
	"""

	def __init__(
			self,
			device_id: int,
			display_name: str = '',
			driver_version: str = '',
			firmware_version: str = '',
			model_number: str = '',
			ordinal_number: int = 0,
			serial_number: str = '',
			type_: int = 0,
			stored_data_type: int = 0,
			delay: int = 0,
			vendor: int = 0
			):

		super().__init__()

		self.device_id = int(device_id)
		self.display_name = str(display_name)
		self.driver_version = str(driver_version)
		self.firmware_version = str(firmware_version)
		self.model_number = str(model_number)
		self.ordinal_number = int(ordinal_number)
		self.serial_number = str(serial_number)
		self.type_ = int(type_)  # TODO
		self.stored_data_type = int(stored_data_type)  # TODO
		self.delay = int(delay)  # TODO
		self.vendor = int(vendor)  # TODO

	__slots__ = [
			"device_id",
			"display_name",
			"driver_version",
			"firmware_version",
			"model_number",
			"ordinal_number",
			"serial_number",
			"type_",
			"stored_data_type",
			"delay",
			"vendor",
			]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Device":
		"""
		Construct a :class:`~.Device` object from an XML element.

		:param element: The XML element to parse the data from.
		"""

		return cls(
				device_id=element.attrib["DeviceID"],
				**tag2dict(element, camel_lookup={"Name": "display_name", "Type": "type_"})
				)


class DeviceList(XMLList):
	"""
	Represents a list of devices in ``Devices.xml``.

	:param version:
	:param devices:
	"""

	def __init__(self, version: int, devices: Optional[Sequence[Device]] = None):
		super().__init__(version, devices)

	with importlib_resources.path(agilent_xsd, "Devices.xsd") as schema_path:
		_schema = str(schema_path)
	_content_type = Device
	_content_xml_name = "Device"

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "DeviceList":
		"""
		Construct a :class:`~.DeviceList` object from an XML element.

		:param element: The XML element to parse the data from.
		"""

		devices = cls(element.Version)
		devices._append_from_element(element)
		return devices


def read_devices_xml(base_path: PathLike) -> DeviceList:
	"""
	Construct a :class:`~.DeviceList` object from the ``DeviceList.xml``
	file in the given directory.

	:param base_path:
	"""

	return DeviceList.from_xml_file(pathlib.Path(base_path) / "Devices.xml")
