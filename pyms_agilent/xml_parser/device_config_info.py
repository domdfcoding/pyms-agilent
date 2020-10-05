#  !/usr/bin/env python
#
#  device_config_info.py
"""
Parser for ``DeviceConfigInfo.xml``.  # noqa D400
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import pathlib
from typing import Sequence

# 3rd party
import attr
import lxml.objectify  # type: ignore
from attr_utils.docstrings import add_attrs_doc
from attr_utils.serialise import serde
from domdf_python_tools.bases import Dictable
from domdf_python_tools.typing import PathLike
from mh_utils.xml import XMLFileMixin

# this package
from .core import make_from_element

__all__ = ["Device", "Parameter", "DeviceConfigInfo", "read_device_config_xml"]


@serde
@add_attrs_doc
@attr.s(slots=True)
class Device:
	"""
	Represents a device in ``DeviceConfigInfo.xml``.

	:param device_id: The ID of the device.
	:param display_name: The display name of the device.
	"""

	device_id: str = attr.ib(converter=str)
	display_name: str = attr.ib(converter=str)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Device":
		"""
		Construct a :class:`~.Device` object from an XML element.

		:param element: The XML element to parse the data from
		"""

		return cls(
				device_id=element.DeviceID,
				display_name=element.DisplayName,
				)


class Parameter(Dictable):
	"""
	Represents a configuration parameter in ``DeviceConfigInfo.xml``.

	:param display_name: The display name of this parameter.
	:param device_id: The ID of the device this parameter configures.
	:param resource_name: The name of the resource this parameter corresponds to.
	:param resource_id: The ID of the resource this parameter corresponds to.
	:param value: The value of this parameter.
	:param units: The unit(s) of this parameter.
	"""

	def __init__(
			self,
			display_name: str,
			device_id: str,
			resource_name: str,
			resource_id: str,
			value: str = '',
			units: str = '',
			):

		super().__init__()

		self.device_id = str(device_id)
		self.resource_name = str(resource_name)
		self.resource_id = str(resource_id)
		self.value = str(value)
		self.units = str(units)
		self.display_name = str(display_name)

	__slots__ = ["device_id", "resource_name", "resource_id", "value", "units", "display_name"]

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Parameter":
		"""
		Construct a :class:`~.Parameter` object from an XML element.

		:param element: The XML element to parse the data from.
		"""

		return cls(
				device_id=element.DeviceID,
				resource_name=element.ResourceName,
				resource_id=element.ResourceID,
				value=element.Value,
				units=element.Units,
				display_name=element.DisplayName,
				)

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	def __repr__(self):
		return f"<{self.__class__.__name__}({self.display_name})>"


class DeviceConfigInfo(XMLFileMixin, Dictable):
	"""
	Represents the device configuration parsed from ``DeviceConfigInfo.xml``.

	:param parameters: List of configuration parameters
	:param devices: List of devices
	"""

	def __init__(self, parameters: Sequence[Parameter], devices: Sequence[Device]):
		super().__init__()

		self.parameters = list(parameters)
		self.devices = list(devices)

	__slots__ = ["parameters", "devices"]

	@property
	def __dict__(self):
		return {
				"parameters": self.parameters,
				"devices": self.devices,
				}

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "DeviceConfigInfo":
		"""
		Construct a :class:`~.DeviceConfigInfo` object from an XML element.

		:param element: The XML element to parse the data from.
		"""

		devices = []
		for device in make_from_element(element, "Device", Device):
			devices.append(device)

		parameters = []
		for parameter in make_from_element(element, "Parameter", Parameter):
			parameters.append(parameter)

		return cls(parameters, devices)


def read_device_config_xml(base_path: PathLike) -> DeviceConfigInfo:
	"""
	Construct a :class:`~.DeviceConfigInfo` object from the ``DeviceConfigInfo.xml``
	file in the given directory.

	:param base_path:
	"""  # noqa D400

	return DeviceConfigInfo.from_xml_file(pathlib.Path(base_path) / "DeviceConfigInfo.xml")
