from pprint import pformat
from typing import Iterable, List, NamedTuple, Tuple, Type, TYPE_CHECKING, Union

import numpy  # type: ignore
import pandas  # type: ignore

from pyms_agilent.enums import DeviceType

# if TYPE_CHECKING:
from pyms_agilent.mhdac.agilent import DataAnalysis


class Range(NamedTuple):
	"""
	2-component named tuple representing a range (start, end)
	"""

	start: float
	stop: float

	@classmethod
	def from_dotnet(cls, irange_object: "DataAnalysis.IRange"):
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


polarity_map = {1: "-", 0: "+", 3: "+-", 2: None}


def ranges_from_list(list_of_irange: Iterable) -> List[Range]:
	"""
	Given a .NET array of IRange objects, return a list of :class:`pyms_agilent.utils.Range` objects.

	:param list_of_irange:
	"""

	return [Range.from_dotnet(r) for r in list_of_irange]


def head(obj: Union[Tuple, List, pandas.DataFrame, pandas.Series, numpy.ndarray], n: int = 10) -> str:
	"""
	Returns the head of the given object.

	:param obj:
	:param n: Show the first ``n`` items of ``obj``.
	"""

	class E(str):
		def __repr__(self) -> str:
			return "..."

	if len(obj) < n:
		return repr(obj)

	if isinstance(obj, tuple) and hasattr(obj, "_fields"):
		# Likely a namedtuple
		head_of_namedtuple = {k: v for k, v in zip(obj._fields[:n], obj[:n])}  # type: ignore
		repr_fmt = '(' + ', '.join(f'{k}={v!r}' for k, v in head_of_namedtuple.items()) + ', ...)'
		return obj.__class__.__name__ + repr_fmt
	elif isinstance(obj, (list, tuple)):
		return pformat(obj.__class__((*obj[:10], E())))
	elif isinstance(obj, (pandas.DataFrame, pandas.Series)):
		return str(obj.head(n))

	return str(obj)



#
# from collections import namedtuple
#
# foo = namedtuple("foo", "a, b, c, d, e, f, g, h, i, j, k, l, m")
#
# print(head(foo(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)))
# print(head(foo(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), 13))
# print(head((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)))
# print(head([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]))
#

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


class DeviceInfo:
	"""
	Information about a device. Used to obtain information about non-MS signals.
	"""

	def __init__(self, name: str, device_type: DeviceType, ordinal: int = 1):
		self._device = DataAnalysis.IDeviceInfo(DataAnalysis.DeviceInfo())
		self._device.DeviceName = str(name)
		self._device.DeviceType = int(device_type)  # type: ignore
		self._device.OrdinalNumber = int(ordinal)


class Interface(NamedTuple):
	"""
	Namedtuple to store the accessor and interface for a class in the MHDAC library.
	"""

	accessor: object
	interface: Type


def datatable2dataframe(datatable) -> pandas.DataFrame:
	"""
	Converts a dotNET ``System.Data.DataTable`` object to a pandas data frame.

	:param datatable:

	:return:
	"""

	return pandas.DataFrame(
			columns=[column.Caption for column in list(datatable.Columns)],
			data=[list(row.ItemArray) for row in list(datatable.Rows)]
			)
