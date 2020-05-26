#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  MSActualDefs.py
"""
Parser for MSActualDefs.py
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
import importlib_resources
from domdf_python_tools.bases import Dictable, namedlist

# this package
from pyms_agilent.xml_parser import agilent_xsd
from .core import get_data_from_element, make_from_element, VersionedList, XMLFileMixin


class ActualType(Dictable):
	"""
	DefaultMassCal::StepType
	"""

	def __init__(
			self,
			ActualID,
			DisplayName='',
			DataType=0,
			DisplayFormat=0,
			DisplayEffects=0,
			DisplayDigits=0,
			Unit='',
			Category='',
			):
		"""
		
		:param ActualID:
		:type ActualID:
		:param DisplayName:
		:type DisplayName: str
		:param DataType: 4 = 64bit integer, 6 = 64bit double
		:type DataType: int
		TODO: enum
		:param DisplayFormat:
		:type DisplayFormat: int
		TODO: enum
		:param DisplayEffects:
		:type DisplayEffects: int
		TODO: enum
		:param DisplayDigits:
		:type DisplayDigits: int
		TODO: enum
		:param Unit:
		:type Unit: str
		:param Category:
		:type Category: str
		"""

		super().__init__()
		
		self.ActualID = int(ActualID)
		self.DisplayName = str(DisplayName)
		self.DataType = int(DataType)
		self.DisplayFormat = int(DisplayFormat)
		self.DisplayEffects = int(DisplayEffects)
		self.DisplayDigits = int(DisplayDigits)
		self.Unit = str(Unit)
		self.Category = str(Category)

	@property
	def __dict__(self):
		return dict(
				ActualID=self.ActualID,
				DisplayName=self.DisplayName,
				DataType=self.DataType,
				DisplayFormat=self.DisplayFormat,
				DisplayEffects=self.DisplayEffects,
				DisplayDigits=self.DisplayDigits,
				Unit=self.Unit,
				Category=self.Category,
				)

	@classmethod
	def from_xml(cls, element):
		ActualID = element.attrib["ActualID"]

		data = dict(
				DisplayName='',
				DataType=0,
				DisplayFormat=0,
				DisplayEffects=0,
				DisplayDigits=0,
				Unit='',
				Category='',
				)
		
		data = get_data_from_element(data, element)
		
		return cls(ActualID, **data)


class ActualsDef(XMLFileMixin, VersionedList):
	"""
	MSActualDef::ActualsDef
	"""
	
	def to_dict(self):
		return dict(
				Version=self.Version,
				all_actuals=list(self),
				)
	with importlib_resources.path(agilent_xsd, "MSActualDefs.xsd") as schema_path:
		_schema = str(schema_path)
	
	@classmethod
	def from_xml(cls, element):
		
		all_actuals = super().from_xml(element)
		
		for Actuals in element.findall("Actuals"):
			actuals = ActualsList(Actuals.attrib["Type"], [])
			
			for Actual in make_from_element(Actuals, "Actual", ActualType):
				actuals.append(Actual)
				print(dict(Actual))
			
			all_actuals.append(actuals)
		
		return all_actuals
	

class ActualsList(namedlist()):
	"""
	MSActualDef::Actuals
	"""
	
	def __init__(
			self,
			Type,
			actuals=None
			):
		"""

		:param Type:
		:type Type: int
		:param actuals:
		:type actuals: List[Actual]
		"""
		
		super().__init__(actuals)
		
		self.Type = int(Type)
		
	def to_dict(self):
		return dict(
				Type=self.Type,
				actuals=list(self),
				)


def read_ms_actuals_defs(base_path):
	return ActualsDef.from_xml_file(base_path / "MSActualDefs.xml")
