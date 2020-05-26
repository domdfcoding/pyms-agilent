#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  AcqMethod.py
"""
Parser for AcqMethod.py
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


# 3rd party


# stdlib
import copy
import pathlib
from collections import namedtuple

# 3rd party
from domdf_python_tools.bases import Dictable

# this package
from .core import make_from_element, XMLFileMixin


class Device(namedtuple("__BaseDevice", "DeviceID, DisplayName, IsRCDevice")):
	"""
	:param DeviceID:
	:type DeviceID: str
	:param DisplayName:
	:type DisplayName: str
	:param IsRCDevice:
	:type IsRCDevice: str
	"""

	__slots__ = []

	def __new__(cls, DeviceID, DisplayName, IsRCDevice):
		return super().__new__(cls, str(DeviceID), str(DisplayName), str(IsRCDevice))

	@classmethod
	def from_xml(cls, element):
		DeviceID = getattr(element, "{http://tempuri.org/DataFileReport.xsd}DeviceId")
		DisplayName = element.DisplayName
		IsRCDevice = element.IsRCDevice
		return cls(DeviceID=DeviceID, DisplayName=DisplayName, IsRCDevice=IsRCDevice)


class AcqMethod(XMLFileMixin, Dictable):
	def __init__(self, parameters, devices):
		"""

		:param parameters:
		:type parameters: List[Parameter]
		:param devices:
		:type devices: List[Device]
		"""

		super().__init__()

		self.parameters = copy.deepcopy(parameters)
		self.devices = copy.deepcopy(devices)

	__slots__ = ["parameters", "devices"]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	@classmethod
	def from_xml(cls, element):

		devices = []

		for device in make_from_element(element, "{http://tempuri.org/DataFileReport.xsd}Devices", Device):
			devices.append(device)

		method_report = MethodReport.from_xml(element.MethodReport)

		# parameters = []
		# for parameter in make_from_element(element, "Parameter", Parameter):
		# 	parameters.append(parameter)
		#
		# return cls(parameters, devices)




class MethodReport(Dictable):
	"""
	AcqMethod::MethodReport
	"""
	def __init__(self, version, name, filename):
		"""

		:param version:
		:type version: float
		:param name:
		:type name: str
		:param filename:
		:type filename: str or pathlib.Path
		"""

		super().__init__()

		self.version = version
		self.name = str(name)
		self.filename = pathlib.Path(filename)

	__slots__ = ["version", "name", "filename"]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	@classmethod
	def from_xml(cls, element):

		version = float(element.Version)
		method_name = str(element.MethodName)
		method_path = pathlib.Path(str(element.MethodPath))
		rc_devices_xml = element.RCDevicesXml
		scic_devices_xml = element.SCICDevicesXml

		print(version)
		print(method_name)
		print(method_path)
		# input(">")

		with open(pathlib.Path("/media/VIDEO/Syncthing/Python/00 Projects/agilent_test/AcqMethod_xml/RCDevices.xml"), "w") as fp:
			fp.write(str(rc_devices_xml))

		# print(rc_devices_xml)
		# print(scic_devices_xml)

		# parameters = []
		# for parameter in make_from_element(element, "Parameter", Parameter):
		# 	parameters.append(parameter)
		#
		# return cls(parameters, devices)


class RCDevices(Dictable):
	"""
	AcqMethod::RCDevices
	"""
	def __init__(self, version, name, filename):
		"""

		:param version:
		:type version: float
		:param name:
		:type name: str
		:param filename:
		:type filename: str or pathlib.Path
		"""

		super().__init__()

		self.version = version
		self.name = str(name)
		self.filename = pathlib.Path(filename)

	__slots__ = ["version", "name", "filename"]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	@classmethod
	def from_xml(cls, element):

		version = float(element.Version)
		method_name = str(element.MethodName)
		method_path = pathlib.Path(str(element.MethodPath))
		rc_devices_xml = element.RCDevicesXml
		scic_devices_xml = element.SCICDevicesXml

		print(version)
		print(method_name)
		print(method_path)
		# input(">")

		with open(pathlib.Path("/media/VIDEO/Syncthing/Python/00 Projects/agilent_test/AcqMethod_xml/RCDevices.xml"), "w") as fp:
			fp.write(str(rc_devices_xml))

		# print(rc_devices_xml)
		# print(scic_devices_xml)

		# parameters = []
		# for parameter in make_from_element(element, "Parameter", Parameter):
		# 	parameters.append(parameter)
		#
		# return cls(parameters, devices)





def read_acqmethod(base_path):
	return AcqMethod.from_xml_file(base_path / "AcqMethod.xml")

