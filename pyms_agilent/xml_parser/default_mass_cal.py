#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  default_mass_cal.py
"""
Parser for default_mass_cal.py
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
from typing import Dict, Optional, Sequence, Union

# 3rd party
import importlib_resources
import lxml.objectify
from domdf_python_tools.bases import Dictable, NamedList, namedlist
from domdf_python_tools.typing import PathLike

# this package
from pyms_agilent.xml_parser import agilent_xsd

# this package
from .core import XMLList, _get_from_enum, make_from_element
from .enums import CalibrationFormulaEnum, CalibrationTechniqueEnum


class StepType(Dictable):
	"""
	Represents a step in a mass calibration, parsed from DefaultMassCal.xml

	:param number:
	:param calibration_technique:
	:type calibration_formula:
	:param number_of_coefficients:
	:param value_use_flags:
	:param values: Dictionary of `Number`: `Value` pairs
	"""

	def __init__(
			self,
			number: int,
			calibration_technique: Union[str, CalibrationTechniqueEnum] = CalibrationTechniqueEnum.Undefined,
			calibration_formula: Union[str, CalibrationFormulaEnum] = CalibrationFormulaEnum.Undefined,
			number_of_coefficients: int = 0,
			value_use_flags: int = 0,
			values: Optional[Dict[int, float]] = None,
			):

		super().__init__()

		self.number = int(number)
		self.calibration_technique = _get_from_enum(calibration_technique, CalibrationTechniqueEnum)
		self.calibration_formula = _get_from_enum(calibration_formula, CalibrationFormulaEnum)
		self.number_of_coefficients = int(number_of_coefficients)
		self.value_use_flags = int(value_use_flags)

		self.values = {}
		if isinstance(values, dict):
			for num, value in values.items():
				self.values[int(num)] = float(value)

	__slots__ = [
			"number",
			"calibration_technique",
			"calibration_formula",
			"number_of_coefficients",
			"value_use_flags",
			"values",
			]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "StepType":
		"""
		Construct a :class:`~.StepType` object from an XML element.

		:param element: The XML element to parse the data from
		"""

		values = {}

		values_tag = element.findall("Values")
		if values_tag:
			value_list = values_tag[0].findall("Value")

			for value in value_list:
				values[value.attrib["Number"]] = value

		return cls(
				number=element.attrib["Number"],
				calibration_technique=element.CalibrationTechnique,
				calibration_formula=element.CalibrationFormula,
				number_of_coefficients=element.NumberOfCoefficients,
				value_use_flags=element.ValueUseFlags,
				values=values,
				)


class Calibration(NamedList):
	"""
	Represents a mass calibration parsed from DefaultMassCal.xml

	:param calibration_id: The ID of the calibration data.
	:param steps: Sequence of calibration steps.
	"""

	def __init__(
			self,
			calibration_id: int,
			steps: Optional[Sequence[StepType]] = None,
			):

		super().__init__(steps)

		self.calibration_id = int(calibration_id)

	_content_type = StepType
	_content_xml_name = "Step"

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Calibration":
		"""
		Construct a :class:`~.Calibration` object from an XML element.

		:param element: The XML element to parse the data from
		"""

		class_ = cls(element.attrib["DefaultCalibrationID"])

		for item in make_from_element(element, cls._content_xml_name, cls._content_type):
			class_.append(item)

		return class_


class CalibrationList(XMLList):
	"""
	Represents a list of mass calibrations in DefaultMassCal.xml

	:param version: The version number of the calibration data.
	:param default_calibrations:
	"""

	def __init__(
			self,
			version: int,
			default_calibrations: Optional[Sequence[Calibration]] = None,
			):
		super().__init__(int(version), default_calibrations)

	with importlib_resources.path(agilent_xsd, "DefaultMassCal.xsd") as schema_path:
		_schema = str(schema_path)
	_content_type = Calibration
	_content_xml_name = "DefaultCalibration"

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "CalibrationList":
		"""
		Construct a :class:`~.CalibrationList` object from an XML element.

		:param element: The XML element to parse the data from
		"""

		class_ = cls(element.Version)
		class_._append_from_element(element.DefaultCalibrations)
		return class_


def read_mass_cal_xml(base_path: PathLike) -> CalibrationList:
	"""
	Construct a :class:`~.CalibrationList` object from the ``DefaultMassCal.xml`` file in the given directory.

	:param base_path:
	"""

	return CalibrationList.from_xml_file(pathlib.Path(base_path) / "DefaultMassCal.xml")
