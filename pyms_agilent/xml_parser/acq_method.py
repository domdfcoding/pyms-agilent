#  !/usr/bin/env python
#
#  acq_method.py
"""
Parser for :file:`{<datafile>}.d/AcqData/AcqMethod.xml`.
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
from pprint import pprint
from typing import Any, Dict, List, Sequence

# 3rd party
import attr
import lxml.objectify  # type: ignore
from attr_utils.docstrings import add_attrs_doc
from attr_utils.serialise import serde
from domdf_python_tools.bases import Dictable
from domdf_python_tools.doctools import prettify_docstrings
from domdf_python_tools.typing import PathLike
from domdf_python_tools.utils import strtobool
from lxml import objectify
from mh_utils.xml import XMLFileMixin

# this package
from .core import make_from_element, tag2dict

__all__ = ["Device", "AcqMethod", "read_acqmethod"]


@add_attrs_doc
@serde
@attr.s(slots=True)
class Device:
	"""
	Represents a device in a :class:`~.AcqMethod:`.

	:param device_id: The ID of the device
	:param display_name: The display name for the device.
	:param rc_device: Flag to indicate the device is an RC Device. If :py:obj:`False` the device is an SCIC.
	:param configuration: List of key: value mappings for configuration options.
	"""

	device_id: str = attr.ib(converter=str)
	display_name: str = attr.ib(converter=str)
	rc_device: bool = attr.ib(converter=strtobool)
	configuration: List[Dict[str, Any]] = attr.ib(converter=list, default=attr.Factory(list))

	@classmethod
	def from_xml(cls, element):
		"""
		Create a :class:`~.Device` object from an XML element.

		:param element: The XML element to parse the data from
		"""
		return cls(
				device_id=getattr(element, "{http://tempuri.org/DataFileReport.xsd}DeviceId"),
				display_name=element.DisplayName,
				rc_device=strtobool(str(element.IsRCDevice)),
				)


@prettify_docstrings
class AcqMethod(XMLFileMixin, Dictable):
	"""
	Represents the method used to acquire data.

	:param version: The version of the method report.
	:param name: The name of the method
	:param filename: The original filename of the method
	:param devices: List of devices used to acquire the data.
	"""

	def __init__(
			self,
			version: float,
			name: str,
			filename: PathLike,
			devices: Sequence[Device] = (),
			):

		super().__init__()

		self.version = float(version)
		self.name = str(name)
		self.filename = pathlib.Path(filename)
		self.devices: List[Device] = list(devices)

	__slots__ = ["version", "name", "filename", "devices"]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "AcqMethod":
		"""
		Construct an :class:`~.AcqMethod` object from an XML element.

		:param element: The XML element to parse the data from
		"""

		version = float(element.MethodReport.Version)  # method report version number
		method_name = str(element.MethodReport.MethodName)  # original method filename
		method_path = pathlib.Path(str(element.MethodReport.MethodPath))  # full original path to method file

		parser = objectify.makeparser(schema=None)

		# embedded XML of rc devices
		rc_devices_xml = objectify.fromstring(str(element.MethodReport.RCDevicesXml), parser=parser)

		# embedded XML of scic devices
		scic_devices_xml = objectify.fromstring(str(element.MethodReport.SCICDevicesXml), parser=parser)

		devices: List[Device] = []

		for device in make_from_element(element, "{http://tempuri.org/DataFileReport.xsd}Devices", Device):
			devices.append(device)

		for section in rc_devices_xml.findall("{http://tempuri.org/DSRdlReport.xsd}Section"):
			section_data = tag2dict(section, xmlns="http://tempuri.org/DSRdlReport.xsd")
			for device in devices:
				if section_data["module_display_name"] == device.display_name and device.rc_device:
					device.configuration.append(section_data)
					break
			else:  # pragma: no cover
				raise ValueError(f"Unknown Device {section_data['module_display_name']}")

		# pprint(devices)

		for section in scic_devices_xml.findall("SectionInfo"):
			section_data = tag2dict(section)
			for device in devices:
				if device.device_id.endswith(section_data["repeater_id1"]) and not device.rc_device:
					device.configuration.append(section_data)
					break
			else:  # pragma: no cover
				raise ValueError(f"Unknown Device {section_data['name']}")

		return cls(
				version=version,
				name=method_name,
				filename=method_path,
				devices=devices,
				)


def read_acqmethod(base_path: PathLike) -> AcqMethod:
	"""
	Construct an :class:`~.AcqMethod` object from the :file:`AcqMethod.xml` file in the given directory.

	:param base_path: Directory containing the :file:`AcqMethod.xml` file.
	"""

	return AcqMethod.from_xml_file(pathlib.Path(base_path) / "AcqMethod.xml")
