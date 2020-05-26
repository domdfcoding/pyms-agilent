#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  Devices.py
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#


# stdlib
import copy
from functools import lru_cache

# 3rd party
import importlib_resources
from domdf_python_tools.bases import Dictable

# this package
from pyms_agilent.xml_parser import agilent_xsd
from .core import get_data_from_element, XMLList


class Device(Dictable):
	def __init__(
			self, DeviceID, Name='', DriverVersion='', FirmwareVersion='', ModelNumber='',
			OrdinalNumber=0, SerialNumber='', Type=0, StoredDataType=0, Delay=0,
			Vendor=0):
		"""
		
		:param DeviceID:
		:type DeviceID: int
		:param Name:
		:type Name: str
		:param DriverVersion:
		:type DriverVersion: str
		:param FirmwareVersion:
		:type FirmwareVersion: str
		:param ModelNumber:
		:type ModelNumber: str
		:param OrdinalNumber:
		:type OrdinalNumber: int
		:param SerialNumber:
		:type SerialNumber: int
		TODO: Enum
		:param Type:
		:type Type: int
		TODO: Enum
		:param StoredDataType:
		:type StoredDataType: int
		TODO: Enum
		:param Delay:
		:type Delay: int
		TODO: Enum
		:param Vendor:
		:type Vendor: int
		TODO: Enum
		"""
		
		super().__init__()
		
		self.DeviceID = int(DeviceID)
		self.Name = str(Name)
		self.DriverVersion = str(DriverVersion)
		self.FirmwareVersion = str(FirmwareVersion)
		self.ModelNumber = str(ModelNumber)
		self.OrdinalNumber = int(OrdinalNumber)
		self.SerialNumber = str(SerialNumber)
		self.Type = Type
		self.StoredDataType = StoredDataType
		self.Delay = Delay
		self.Vendor = Vendor

	@property
	def __dict__(self):
		return dict(
				DeviceID=self.DeviceID,
				Name=self.Name,
				DriverVersion=self.DriverVersion,
				FirmwareVersion=self.FirmwareVersion,
				ModelNumber=self.ModelNumber,
				OrdinalNumber=self.OrdinalNumber,
				SerialNumber=self.SerialNumber,
				Type=self.Type,
				StoredDataType=self.StoredDataType,
				Delay=self.Delay,
				Vendor=self.Vendor,
				)

	@classmethod
	def from_xml(cls, element):
		data = dict(
				DeviceID=0, Name='', DriverVersion='', FirmwareVersion='',
				ModelNumber='', OrdinalNumber=0, SerialNumber='', Type=0,
				StoredDataType=0, Delay=0, Vendor=0
				)
		
		return cls(**get_data_from_element(data, element))


class DeviceList(XMLList):
	def __init__(self, Version, devices=None):
		"""

		:param Version:
		:type Version: int
		:param devices:
		:type devices: List[Device]
		"""
		
		super().__init__(Version, copy.deepcopy(devices))
	
	def to_dict(self):
		return dict(
				Version=self.Version,
				devices=list(self),
				)
	
	@lru_cache()
	def get_device(self, DeviceID):
		"""

		:param DeviceID:
		:type DeviceID: str

		:return:
		:rtype:
		"""
		
		for device in self:
			if device.DeviceID == DeviceID:
				return device

	with importlib_resources.path(agilent_xsd, "Devices.xsd") as schema_path:
		_schema = str(schema_path)
	_content_type = Device
	_content_xml_name = "Device"
	
	@classmethod
	def from_xml(cls, element):
		devices = super().from_xml(element)
		devices._append_from_element(element)
		
		return devices


def read_devices_xml(base_path):
	return DeviceList.from_xml_file(base_path / "Devices.xml")
