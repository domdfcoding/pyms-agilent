#!/usr/bin/env python
#
#  sample_info.py
"""
Parser for ``sample_info.xml``.
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
from typing import Any, List

# 3rd party
import attr
import importlib_resources
import lxml.objectify  # type: ignore
from attr_utils.pprinter import pretty_repr
from attr_utils.serialise import serde
from domdf_python_tools.utils import strtobool
from mh_utils.utils import strip_string

# this package
from pyms_agilent.xml_parser import agilent_xsd

# this package
from .core import XMLList

__all__ = ["Field", "SampleInfo", "read_sample_info_xml"]


@serde
@pretty_repr
@attr.s(slots=True)
class Field:
	"""
	Represents a field in ``sample_info.xml``.

	.. TODO:: Enum for data_type
	"""

	#: The name of the field.
	name: str = attr.ib(converter=strip_string, default='')

	#: The display name of the field.
	display_name: str = attr.ib(converter=strip_string, default='')

	#: The value of the field.
	value: Any = attr.ib(default='')

	#: The type of data in the field.
	data_type: int = attr.ib(converter=int, default=0)

	#: The units of the data in the field.
	units: str = attr.ib(converter=strip_string, default='')

	#: The type of field.
	field_type: str = attr.ib(converter=strip_string, default='')

	#: Whether the field is overridden.
	overridden: bool = attr.ib(converter=strtobool, default=False)

	@classmethod
	def from_xml(cls, element):
		"""
		Create a :class:`~.Field` object from an XML element.

		:param element: The XML element to parse the data from
		"""

		return cls(
				name=str(element.Name),
				display_name=str(element.DisplayName),
				data_type=int(element.DataType),
				units=str(element.Units),
				field_type=str(element.FieldType),
				overridden=strtobool(str(element.Overridden)),
				value=element.Value.text
				)


class SampleInfo(XMLList):
	"""
	List of information about the sample, parsed from ``sample_info.xml``.

	Each piece of information is represented as a :class:`.~Field`

	:param version: The version number of the sample info data.
	:param fields:
	"""

	def __init__(
			self,
			version: int,
			fields: List[Field] = None,
			):

		super().__init__(version, fields)

		self.version = int(version)

	_content_type = Field
	_content_xml_name = "Field"

	with importlib_resources.path(agilent_xsd, "sample_info.xsd") as path:
		_schema = str(path)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "SampleInfo":
		"""
		Construct a :class:`~.SampleInfo` object from an XML element.

		:param element: The XML element to parse the data from
		"""

		version = int(element.Version)  # sample_info version number

		obj = cls(version)
		obj._append_from_element(element)
		return obj


def read_sample_info_xml(base_path) -> "SampleInfo":
	"""
	Construct an :class:`~.SampleInfo` object from the ``sample_info.xml`` file in the given directory.

	:param base_path:
	"""

	return SampleInfo.from_xml_file(pathlib.Path(base_path) / "sample_info.xml")
