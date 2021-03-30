#  !/usr/bin/env python
#
#  utils.py
"""
General utility functions.
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
import enum
import math
from typing import Any, Callable, Iterable, List, NamedTuple, Type

# 3rd party
import enum_tools
import pandas  # type: ignore
from attr_utils.pprinter import register_pretty
from domdf_python_tools.doctools import prettify_docstrings

# this package
from pyms_agilent.mhdac.agilent import DataAnalysis

__all__ = [
		"Range",
		"polarity_map",
		"ranges_from_list",
		"frozen_comparison",
		"Interface",
		"datatable2dataframe",
		"isnan"
		]


@prettify_docstrings
class Range(NamedTuple):
	"""
	2-component named tuple representing a range (start, end).
	"""

	start: float
	stop: float

	@classmethod
	def from_dotnet(cls, irange_object: "DataAnalysis.IRange"):  # pragma: no cover (!Windows)
		"""
		Construct a :class:`~.Range` from a Python.NET object.

		:param irange_object:
		"""

		return cls(irange_object.Start, irange_object.End)

	#
	# def ValueString(self):
	# 	"""
	# 	Returns a string representing the time range,
	# 		to 2 decimal places
	#
	# 	:return:
	# 	"""
	#
	# 	return self.IRange.ValueString(True)[1]
	#
	# def ExtendedValueString(self):
	# 	"""
	# 	Returns a string representing the time range,
	# 		to 5 decimal places
	#
	# 	:return:
	# 	"""
	#
	# 	return self.IRange.ExtendedValueString(True)[1]
	#
	# def __copy__(self):
	# 	return self.__class__(self.IRange.Clone())
	#
	# # The following methods copied from ScanWindow in
	# # 	ms_deisotope.data_source.metadata.scan_traits
	#
	# def is_empty(self):
	# 	if self.start is None:
	# 		return self.end is None
	# 	return self.start == self.end == 0.0
	#
	# def __nonzero__(self):
	# 	return not self.is_empty()
	#
	# def __bool__(self):
	# 	return self.__nonzero__()


polarity_map = {1: '-', 0: '+', 3: "+-", 2: None}


def ranges_from_list(list_of_irange: Iterable) -> List[Range]:  # pragma: no cover (!Windows)
	"""
	Given a .NET array of IRange objects, return a list of :class:`pyms_agilent.utils.Range` objects.

	:param list_of_irange:
	"""

	return [Range.from_dotnet(r) for r in list_of_irange]


# class Device:
# 	"""
# 	Represents a device in the instrument configuration.
# 	"""
#
# 	def __init__(self):
#
# 		self.data_reader = DataAnalysis.MassSpecDataReader()
#
# 	@classmethod
# 	def from_dotnet(cls, DeviceInfo):
# 		obj = cls()
# 		obj.data_reader = DeviceInfo
# 		return obj

#
# class DeviceInfo:
# 	"""
# 	Information about a device. Used to obtain information about non-MS signals.
#
# 	:param name:
# 	:param device_type:
# 	:param ordinal:
# 	"""
#
# 	def __init__(self, name: str, device_type: DeviceType, ordinal: int = 1):
# 		self._device = DataAnalysis.IDeviceInfo(DataAnalysis.DeviceInfo())
# 		self._device.DeviceName = str(name)
# 		self._device.DeviceType = int(device_type)  # type: ignore
# 		self._device.OrdinalNumber = int(ordinal)


@prettify_docstrings
class Interface(NamedTuple):
	"""
	2-element to store the accessor and interface for a class in the MHDAC library.
	"""

	#: The accessor object.
	accessor: object

	#: The interface class.
	interface: Type


def datatable2dataframe(datatable) -> pandas.DataFrame:  # pragma: no cover (!Windows)
	"""
	Converts a dotNET :class:`System.Data.DataTable` object to a pandas data frame.

	:param datatable:
	:type datatable: :class:`System.Data.DataTable`
	"""

	return pandas.DataFrame(
			columns=[column.Caption for column in list(datatable.Columns)],
			data=[list(row.ItemArray) for row in list(datatable.Rows)]
			)


@register_pretty(enum.EnumMeta)
@register_pretty(enum.Enum)
@register_pretty(enum.IntEnum)
@register_pretty(enum.Flag)
@register_pretty(enum.IntFlag)
@register_pretty(enum_tools.Enum)
@register_pretty(enum_tools.IntEnum)
@register_pretty(enum_tools.StrEnum)
@register_pretty(enum_tools.AutoNumberEnum)
@register_pretty(enum_tools.OrderedEnum)
@register_pretty(enum_tools.DuplicateFreeEnum)
@register_pretty(enum_tools.Flag)
@register_pretty(enum_tools.IntFlag)
@register_pretty(enum_tools.DocumentedEnum)
def pretty_enum(value, ctx):
	return repr(value)


def isnan(value: Any) -> bool:
	"""
	Returns whether the value is ``float('nan')``.

	Returns :py:obj:`False` if the value is not a :class:`float`.

	:param value:
	"""

	if isinstance(value, float):
		return math.isnan(value)
	else:
		return False


def frozen_comparison(*classes: Type) -> Callable[[Type], Type]:
	"""
	Decorator to add the ``__eq__`` method to classes that compares frozen
	and non frozen versions of a class.

	:param classes:
	"""  # noqa: D400

	def deco(cls: Type) -> Type:

		classes_ = (cls, *classes)

		def __eq__(self, other) -> bool:
			"""
			Returns ``self == other``.
			"""

			if isinstance(other, classes_):
				left = {k: v for k, v in self.to_dict().items() if not isnan(v)}
				right = {k: v for k, v in other.to_dict().items() if not isnan(v)}
				return left == right
			elif isinstance(other, dict):
				left = {k: v for k, v in self.to_dict().items() if not isnan(v)}
				right = {k: v for k, v in other.items() if not isnan(v)}
				return left == right
			return NotImplemented

		cls.__eq__ = __eq__  # type: ignore
		cls.__eq__.__qualname__ = f"{cls.__name__}.__eq__"
		cls.__eq__.__module__ = cls.__module__

		return cls

	return deco
