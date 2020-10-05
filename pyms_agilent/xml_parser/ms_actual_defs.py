#  !/usr/bin/env python
#
#  ms_actual_defs.py
"""
Parser for ``MSActualDefs.xml``.
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
from typing import Callable, Optional, Sequence, Union

# 3rd party
import importlib_resources
import lxml.objectify  # type: ignore
from domdf_python_tools.bases import Dictable
from domdf_python_tools.typing import PathLike
from numpy import float64, int64  # type: ignore

# this package
from pyms_agilent.xml_parser import agilent_xsd

# this package
from .core import XMLList, make_from_element

__all__ = ["Actual", "ActualsDef", "read_ms_actuals_defs"]


@prettify_docstrings
class Actual(Dictable):
	"""
	Periodic/Scan Actual Type information.

	:param actual_id:
	:param display_name:
	:param data_type: 4 = 64bit integer, 6 = 64bit float
	:param display_format:
	:param display_effects:
		TODO: enum
	:param display_digits:
	:param unit:
	:param category:

	.. TODO:: Enums for ``display_format`` and ``display_effects``
	"""

	def __init__(
			self,
			actual_id: int,
			display_name: str = '',
			data_type: Optional[Union[int, Callable]] = None,
			display_format: int = 0,
			display_effects: int = 0,
			display_digits: int = 0,
			unit: str = '',
			category: str = '',
			):

		super().__init__()

		self.actual_id = int(actual_id)
		self.display_name = str(display_name)

		if not callable(data_type) and data_type is not None:
			data_type = int(data_type)

		if data_type is None:
			# Guess based on ActualID
			if 55 <= actual_id < 65 or actual_id > 345:
				self.data_type = int64
			else:
				self.data_type = float64
		elif isinstance(data_type, int):
			# For ActualID >=55 and < 65 or > 345, DataType = 4 (64bit integer)
			# For ALL other index, DataType = 6 (64bit double)
			if data_type == 4:
				self.data_type = int64
			elif data_type == 6:
				self.data_type = float64
			else:
				self.data_type = str
		else:
			self.data_type = data_type

		self.display_format = int(display_format)
		self.display_effects = int(display_effects)
		self.display_digits = int(display_digits)
		self.unit = str(unit)
		self.category = str(category)

	__slots__ = [
			"actual_id",
			"display_name",
			"data_type",
			"display_format",
			"display_effects",
			"display_digits",
			"unit",
			"category",
			]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}({self.display_name!r}, id={self.actual_id})>"

	def __str__(self) -> str:
		return str(self.display_name)

	@classmethod
	def from_xml(cls, element):
		"""
		Create a :class:`~.Actual` object from an XML element.

		:param element: The XML element to parse the data from
		"""

		return cls(
				actual_id=element.attrib["ActualID"],
				display_name=element.DisplayName,
				data_type=element.DataType,
				display_format=element.DisplayFormat,
				display_effects=element.DisplayEffects,
				display_digits=element.DisplayDigits,
				unit=element.Unit,
				category=element.Category,
				)


class ActualsDef(XMLList):
	r"""
	Stores the overall Actual Definition Information for all devices.

	Parsed from ``MSActualDefs.xml``.

	List of :class:`~.Actual` objects.

	:param version: The version of the ``MSActualDefs.xml`` file.
	:param type\_:
	:param actuals:

	.. TODO:: Enum for ``type_``
	"""

	def __init__(
			self,
			version: int,
			type_: int = 0,
			actuals: Sequence[Actual] = None,
			):
		super().__init__(version, actuals)
		self.type_ = int(type_)

	with importlib_resources.path(agilent_xsd, "MSActualDefs.xsd") as schema_path:
		_schema = str(schema_path)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "ActualsDef":
		"""
		Construct an :class:`~.ActualsDef` object from an XML element.

		:param element: The XML element to parse the data from.
		"""

		return cls(
				element.Version,
				element.Actuals.attrib["Type"],
				list(make_from_element(element.Actuals, "Actual", Actual)),  # type: ignore
				)


def read_ms_actuals_defs(base_path: PathLike) -> ActualsDef:
	"""
	Construct an :class:`~.ActualsDef` object from the ``MSActualDefs.xml`` file in the given directory.

	:param base_path:
	"""

	return ActualsDef.from_xml_file(pathlib.Path(base_path) / "MSActualDefs.xml")
