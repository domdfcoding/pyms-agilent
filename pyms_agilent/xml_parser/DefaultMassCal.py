#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  DefaultMassCal.py
"""
Parser for DefaultMassCal.py
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
from .core import _get_from_enum, get_data_from_element, make_from_element, XMLList
from .enums import CalibrationFormulaEnum, CalibrationTechniqueEnum


class StepType(Dictable):
	"""
	DefaultMassCal::StepType
	"""
	
	def __init__(
			self,
			Number,
			CalibrationTechnique=None,
			CalibrationFormula=None,
			NumberOfCoefficients=None,
			ValueUseFlags=None,
			Values=None,
			):
		"""

		:param Number:
		:type Number: int
		:param CalibrationTechnique: str or CalibrationTechniqueEnum
		:type CalibrationTechnique:
		:param CalibrationFormula: str or CalibrationFormulaEnum
		:type CalibrationFormula:
		:param NumberOfCoefficients:
		:type NumberOfCoefficients: int
		:param ValueUseFlags:
		:type ValueUseFlags: int
		:param Values: Dictionary of `Number`: `Value` pairs
		:type Values: dict
		"""
		
		super().__init__()
		
		self.Number = int(Number)
		self.CalibrationTechnique = _get_from_enum(CalibrationTechnique, CalibrationTechniqueEnum)
		self.CalibrationFormula = _get_from_enum(CalibrationFormula, CalibrationFormulaEnum)
		self.NumberOfCoefficients = int(NumberOfCoefficients)
		self.ValueUseFlags = int(ValueUseFlags)

		self.Values = {}
		for num, value in Values.items():
			self.Values[int(num)] = float(value)
	
	__slots__ = [
			"Number", "CalibrationTechnique", "CalibrationFormula",
			"NumberOfCoefficients", "ValueUseFlags", "Values",
			]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)
		
		return data
	
	@classmethod
	def from_xml(cls, element):
		Number = element.attrib["Number"]
		
		data = {
				"CalibrationTechnique": None,
				"CalibrationFormula": None,
				"NumberOfCoefficients": None,
				"ValueUseFlags": None,
				}
		
		data = get_data_from_element(data, element)
		
		data["Values"] = {}
		
		Values = element.findall("Values")
		if Values:
			value_list = Values[0].findall("Value")
			
			for value in value_list:
				data["Values"][value.attrib["Number"]] = value
		
		return cls(Number, **data)


class DefaultCalibrationType(namedlist()):
	"""
	DefaultMassCal::DefaultCalibrationType
	"""
	
	def __init__(
			self,
			DefaultCalibrationID,
			steps=None,
			):
		"""

		:param DefaultCalibrationID:
		:type DefaultCalibrationID: int
		:param steps:
		:type steps: list
		"""
		
		super().__init__(steps)
		
		self.DefaultCalibrationID = int(DefaultCalibrationID)
	
	_content_type = StepType
	_content_xml_name = "Step"
	
	@classmethod
	def from_xml(cls, element):
		DefaultCalibrationID = element.attrib["DefaultCalibrationID"]
		class_ = cls(DefaultCalibrationID)
		
		for item in make_from_element(element, cls._content_xml_name, cls._content_type):
			class_.append(item)
		
		return class_
	
	def to_dict(self):
		return dict(
				DefaultCalibrationID=self.DefaultCalibrationID,
				steps=list(self),
				)


class DefaultMassCalibration(XMLList):
	"""
	DefaultMassCal::DefaultMassCalibration
	"""
	
	def __init__(
			self,
			Version,
			DefaultCalibrations=None,
			):
		"""

		:param Version:
		:type Version: int
		:param DefaultCalibrations:
		:type DefaultCalibrations:
		"""
		
		super().__init__(Version, DefaultCalibrations)
		
	def to_dict(self):
		return dict(
				Version=self.Version,
				DefaultCalibrations=list(self),
				)
	with importlib_resources.path(agilent_xsd, "DefaultMassCal.xsd") as schema_path:
		_schema = str(schema_path)
	_content_type = DefaultCalibrationType
	_content_xml_name = "DefaultCalibration"
	
	@classmethod
	def from_xml(cls, element):
		class_ = super().from_xml(element)
		class_._append_from_element(element.DefaultCalibrations)
		return class_


def read_mass_cal_xml(base_path):
	return DefaultMassCalibration.from_xml_file(base_path / "DefaultMassCal.xml")

