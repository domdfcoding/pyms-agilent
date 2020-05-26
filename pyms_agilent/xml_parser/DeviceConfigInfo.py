#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  DeviceConfigInfo.py
"""
Parser for DeviceConfigInfo.xml
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
from collections import namedtuple
from functools import lru_cache

# 3rd party
from domdf_python_tools.bases import Dictable, namedlist

# this package
from .core import make_from_element, XMLFileMixin


class DeviceList(namedlist()):
	
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


class Device(namedtuple("__BaseDevice", "DeviceID, DisplayName")):
	"""
	:param DeviceID:
	:type DeviceID: str
	:param DisplayName:
	:type DisplayName: str
	"""
	
	__slots__ = []

	def __new__(cls, DeviceID, DisplayName):
		return super().__new__(cls, str(DeviceID), str(DisplayName))
	
	@classmethod
	def from_xml(cls, element):
		DeviceID = element.DeviceID
		DisplayName = element.DisplayName
		return cls(DeviceID=DeviceID, DisplayName=DisplayName)


class Parameter(Dictable):
	def __init__(self, DeviceID, ResourceName, ResourceID, Value, Units, DisplayName):
		"""
		
		:param DeviceID:
		:type DeviceID: str
		:param ResourceName:
		:type ResourceName: str
		:param ResourceID:
		:type ResourceID: str
		:param Value:
		:type Value: str
		:param Units:
		:type Units: str
		:param DisplayName:
		:type DisplayName: str
		"""
		
		super().__init__()
		
		self.DeviceID = str(DeviceID)
		self.ResourceName = str(ResourceName)
		self.ResourceID = str(ResourceID)
		self.Value = str(Value)
		self.Units = str(Units)
		self.DisplayName = str(DisplayName)
	
	__slots__ = ["DeviceID", "ResourceName", "ResourceID", "Value", "Units", "DisplayName"]
	
	@classmethod
	def from_xml(cls, element):
		data = {}
		for key in cls.__slots__:
			data[key] = element[key]
		
		return cls(**data)

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)
		
		return data
	
	def __repr__(self):
		return f"<{self.__class__.__name__}({self.DisplayName})>"


class DeviceConfigInformation(XMLFileMixin, Dictable):
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
		for device in make_from_element(element, "Device", Device):
			devices.append(device)
		
		parameters = []
		for parameter in make_from_element(element, "Parameter", Parameter):
			parameters.append(parameter)
		
		return cls(parameters, devices)


def read_device_config_xml(base_path):
	return DeviceConfigInformation.from_xml_file(base_path / "DeviceConfigInfo.xml")
