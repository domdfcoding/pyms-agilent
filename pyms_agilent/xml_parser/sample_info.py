#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  sample_info.py
"""
Parser for sample_info.xml
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


import distutils.util
from collections import namedtuple

from .core import get_data_from_element, XMLList


class Field(namedtuple('__BaseField', 'Name DisplayName Value DataType Units FieldType Overridden')):
	"""
		
	:param Name:
	:type Name: str
	:param DisplayName:
	:type DisplayName: str
	:param Value:
	:type Value: any
	:param DataType:
	:type DataType: int
	# TODO: enum
	:param Units:
	:type Units: str
	:param FieldType:
	:type FieldType: str
	:param Overridden:
	:type Overridden: bool
	"""

	__slots__ = []
	
	def __new__(cls, Name='', DisplayName='', Value=None, DataType=0, Units='', FieldType='', Overridden=False):

		if isinstance(Overridden, str):
			Overridden = distutils.util.strtobool(Overridden)
		Overridden = bool(Overridden)
		
		return super().__new__(
				cls,
				Name=Name,
				DisplayName=DisplayName,
				Value=Value,
				DataType=DataType,
				Units=Units,
				FieldType=FieldType,
				Overridden=Overridden,
				)
	
	@classmethod
	def from_xml(cls, element):
		
		data = dict(
				Name='', DisplayName='', Value=None, DataType=0,
				Units='', FieldType='', Overridden=False,
				)
		
		return cls(**get_data_from_element(data, element))


class SampleInfo(XMLList):
	"""
	sample_info.xml
	"""
	
	def __init__(
			self,
			Version,
			fields=None,
			):
		"""

		:param Version:
		:type Version: int
		:param fields:
		:type fields: List[Field]
		"""
		
		super().__init__(Version, fields)
		
		self.Version = int(Version)
		
	def to_dict(self):
		return dict(
				Version=self.Version,
				fields=list(self),
				)
	
	_content_type = Field
	_content_xml_name = "Field"
	
	@classmethod
	def from_xml(cls, element):
		class_ = super().from_xml(element)
		class_._append_from_element(element)
		return class_


def read_sample_info_xml(base_path):
	return SampleInfo.from_xml_file(base_path / "sample_info.xml")
