#  !/usr/bin/env python
#
#  chromatograms.py
"""
Classes to access chromatographic data from ``.d`` datafiles.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from abc import ABC
from typing import List, Optional, Sequence, Tuple, Union

# this package
import attr
from attr_utils.docstrings import add_attrs_doc

from pyms_agilent.attrs_serde import serde
from pyms_agilent.enums import (
		ChromType,
		DataUnit,
		DataValueType,
		DeviceType,
		IonizationMode,
		MSLevel,
		MSScanType,
		MSStorageMode
		)
from pyms_agilent.mhdac.agilent import DataAnalysis
from pyms_agilent.utils import Range, polarity_map, ranges_from_list

__all__ = [
	"Signal",
	"FrozenSignal",
	"InstrumentCurve",
	"axis_info_converter",
	"y_axis_info_converter",
	"FrozenInstrumentCurve",
	"TIC",
	]


class Signal(ABC):
	"""
	Abstract base class for instrument signals.
	"""

	#: The .NET interface
	interface: DataAnalysis.IBDAChromData

	#: The .NET class that provides access to the data.
	data_reader: DataAnalysis.BDAChromData

	@property
	def chromatogram_type(self) -> ChromType:
		"""
		Returns the type of chromatogram.
		"""

		return ChromType(self.interface.ChromatogramType)

	@property
	def device_name(self) -> str:
		"""
		Returns the name of the device used to acquire the data.
		"""

		return str(self.interface.DeviceName)

	@property
	def device_type(self) -> DeviceType:
		"""
		Returns the type of device used to acquire the data.
		"""

		return DeviceType(self.interface.DeviceType)

	@property
	def is_chromatogram(self) -> bool:
		"""
		Returns whether the data is a chromatogram.
		"""

		return self.interface.IsChromatogram

	@property
	def is_icp_data(self) -> bool:
		"""
		Returns whether the data is ICP (inductively coupled plasma) data.
		"""

		return self.data_reader.IsICPData

	@property
	def is_cycle_summed(self) -> bool:
		"""
		Returns whether the data is cycle summed.

		.. TODO:: What does this mean?
		"""

		return self.interface.IsCycleSummed

	@property
	def is_mass_spectrum(self) -> bool:
		"""
		Returns whether the data is a mass spectrum.
		"""

		return self.interface.IsMassSpectrum

	@property
	def is_primary_mrm(self) -> bool:
		"""
		If the data was obtained vis Multiple reaction monitoring (MRM):

		* For triggered MRMs:

			+ Returns :py:obj:`True` if the MRM is a primary transition
			+ Returns :py:obj:`False` if the MRM is a triggered transition

		* For non-triggered MRMs (e.g. static, dynamic MRMs):

			+ Returns :py:obj:`True`

		Returns False for all non-MRM chromatograms.
		"""  # noqa D400
		return self.interface.IsPrimaryMrm

	@property
	def is_uv_spectrum(self) -> bool:
		"""
		Returns whether the data is a UV-Vis spectrum.
		"""

		return self.interface.IsUvSpectrum

	@property
	def ordinal_number(self) -> int:
		"""
		Returns the ordinal number of the signal.
		"""

		return int(self.interface.OrdinalNumber)

	@property
	def signal_description(self) -> str:
		"""
		Returns the description for the signal.
		"""

		return str(self.interface.SignalDescription)

	@property
	def signal_name(self) -> str:
		"""
		Returns the name of the signal.
		"""

		return str(self.interface.SignalName)

	@property
	def total_data_points(self) -> int:
		"""
		Returns the total number of data points.
		"""

		return int(self.interface.TotalDataPoints)

	@property
	def x_data(self) -> List[float]:
		"""
		Returns the x-axis data.
		"""

		return list(self.interface.XArray)

	@property
	def y_data(self) -> List[float]:
		"""
		Returns the y-axis data.
		"""

		return list(self.interface.YArray)


@serde
@add_attrs_doc
@attr.s(slots=True, frozen=True)
class FrozenSignal(ABC):
	"""
	Frozen version of :class:`~.Signal`.

	Abstract base class for instrument signals.
	"""

	#: The type of chromatogram.
	chromatogram_type: ChromType = attr.ib(converter=ChromType)

	#: The name of the device used to acquire the data.
	device_name: str = attr.ib(converter=str)

	#: The type of device used to acquire the data.
	device_type: DeviceType = attr.ib(converter=DeviceType)

	#: Whether the data is a chromatogram.
	is_chromatogram: bool = attr.ib(converter=bool)

	#: Whether the data is ICP (inductively coupled plasma) data.
	is_icp_data: bool = attr.ib(converter=bool)

	#: Whether the data is cycle summed.
	is_cycle_summed: bool = attr.ib(converter=bool)

	#: Whether the data is a mass spectrum.
	is_mass_spectrum: bool = attr.ib(converter=bool)

	is_primary_mrm: bool = attr.ib(converter=bool)
	"""
	If the data was obtained vis Multiple reaction monitoring (MRM):

		* For triggered MRMs:

			+ Returns :py:obj:`True` if the MRM is a primary transition
			+ Returns :py:obj:`False` if the MRM is a triggered transition

		* For non-triggered MRMs (e.g. static, dynamic MRMs):

			+ Returns :py:obj:`True`

		Returns False for all non-MRM chromatograms.
	"""

	#: Whether the data is a UV-Vis spectrum.
	is_uv_spectrum: bool = attr.ib(converter=bool)

	#: The ordinal number of the signal.
	ordinal_number: int = attr.ib(converter=int)

	#: The description for the signal.
	signal_description: str = attr.ib(converter=str)

	#: The name of the signal.
	signal_name: str = attr.ib(converter=str)

	#: The total number of data points.
	total_data_points: int = attr.ib(converter=int)

	#: The x-axis data.
	x_data: List[float] = attr.ib(converter=list)

	#: The y-axis data.
	y_data: List[float] = attr.ib(converter=list)


class InstrumentCurve(Signal):
	"""
	Represents data recorded by the instrument.

	:param data_reader: Python.NET object.
	"""

	def __init__(self, data_reader: DataAnalysis.BDAChromData):

		self.data_reader = data_reader
		self.interface = DataAnalysis.IBDAChromData(self.data_reader)

	def get_x_axis_info(self) -> Tuple[DataValueType, DataUnit]:
		"""
		Returns the type of data represented by the x-axis, and the corresponding unit.
		"""

		_, unit, value_type = self.data_reader.GetXAxisInfo(0, 0)
		return DataValueType(value_type), DataUnit(unit)

	def get_y_axis_info(self) -> Tuple[DataValueType, Union[DataUnit, str]]:
		"""
		Returns the type of data represented by the y-axis, and the corresponding unit.
		"""

		_, unit, value_type, label = self.data_reader.GetYAxisInfo(0, 0, '')

		if unit == DataUnit.ResponseUnits:
			return DataValueType(value_type), str(label)
		else:
			return DataValueType(value_type), DataUnit(unit)

	def freeze(self) -> "FrozenInstrumentCurve":
		"""
		Returns a :class:`~pyms_agilent.mhdac.chromatograms.FrozenInstrumentCurve` object
		containing the same data as this object.
		"""

		return FrozenInstrumentCurve(
				chromatogram_type=self.chromatogram_type,
				device_name=self.device_name,
				device_type=self.device_type,
				is_chromatogram=self.is_chromatogram,
				is_icp_data=self.is_icp_data,
				is_cycle_summed=self.is_cycle_summed,
				is_mass_spectrum=self.is_mass_spectrum,
				is_primary_mrm=self.is_primary_mrm,
				is_uv_spectrum=self.is_uv_spectrum,
				ordinal_number=self.ordinal_number,
				signal_description=self.signal_description,
				signal_name=self.signal_name,
				total_data_points=self.total_data_points,
				x_data=self.x_data,
				y_data=self.y_data,
				x_axis_info=self.get_x_axis_info(),
				y_axis_info=self.get_y_axis_info(),
				)


def axis_info_converter(info: Sequence[int]) -> Tuple[DataValueType, DataUnit]:
	"""
	Converter for :meth:`~pyms_agilent.mhdac.chromatograms.InstrumentCurve.get_x_axis_info` in
	:class:`~pyms_agilent.mhdac.chromatograms.InstrumentCurve`.

	:param info: 2-element long sequence comprising the data value type and data unit.

	:return: 2-element tuple comprising :class:`~enum.Enum` members representing the same.
	"""

	value_type, unit, *_ = info
	return DataValueType(value_type), DataUnit(unit)


def y_axis_info_converter(info: Sequence[Union[int, str]]) -> Tuple[DataValueType, Union[DataUnit, str]]:
	"""
	Converter for :meth:`~pyms_agilent.mhdac.chromatograms.InstrumentCurve.get_y_axis_info` in
	:class:`~pyms_agilent.mhdac.chromatograms.InstrumentCurve`.

	:param info: A 2-element long sequence comprising the data value type and either the unit type or a textual unit label.

	:return: 2-element tuple comprising :class:`~enum.Enum` members representing the same.
		If the data value type is :py:enum:mem`~DataUnit.ResponseUnits` the second element will instead be
		the textual label.
	"""

	value_type, unit_or_label, *_ = info

	if isinstance(unit_or_label, str):
		return DataValueType(value_type), unit_or_label
	else:
		return DataValueType(value_type), DataUnit(unit_or_label)


@serde
@add_attrs_doc
@attr.s(slots=True, frozen=True)
class FrozenInstrumentCurve(FrozenSignal):
	"""
	Frozen version of :class:`~.InstrumentCurve`.

	Represents data recorded by the instrument.
	"""

	#: The type of data represented by the x-axis, and the corresponding unit.
	x_axis_info: Tuple[DataValueType, DataUnit] = attr.ib(converter=axis_info_converter)

	#: The type of data represented by the y-axis, and the corresponding unit (which may be a textual label).
	y_axis_info: Tuple[DataValueType, Union[DataUnit, str]] = attr.ib(converter=y_axis_info_converter)

	def get_x_axis_info(self) -> Tuple[DataValueType, DataUnit]:
		"""
		Returns the type of data represented by the x-axis, and the corresponding unit.
		"""

		return self.x_axis_info

	def get_y_axis_info(self) -> Tuple[DataValueType, Union[DataUnit, str]]:
		"""
		Returns the type of data represented by the y-axis, and the corresponding unit.
		"""

		return self.y_axis_info


class TIC(Signal):
	"""
	Represents a Total Ion Chromatogram.

	:param data_reader: Python.NET object.
	"""

	data_reader: DataAnalysis.BDAChromData

	def __init__(self, data_reader: DataAnalysis.BDAChromData):

		self.data_reader = data_reader
		self.interface = DataAnalysis.IBDAChromData(self.data_reader)

	@property
	def abundance_limit(self) -> float:
		"""
		Returns the abundance limit of the TIC data; that is the largest value that could be seen
		in the data (the theoretical "full scale" value).
		"""  # noqa D400

		# Also float(self.data_reader.MSOverallScanRecordInformation.AbundanceLimit)
		return float(self.interface.AbundanceLimit)

	@property
	def acquired_time_ranges(self) -> List[Range]:
		"""
		Returns the list of time ranges over which the data was acquired.

		If the data was acquired over only one time range, the list will contain only one element.
		"""

		return ranges_from_list(self.interface.AcquiredTimeRange)

	@property
	def collision_energy(self) -> float:
		"""
		Returns the collision energy used to acquire the data.
		"""

		# Also float(self.data_reader.MSOverallScanRecordInformation.CollisionEnergy)
		return float(self.interface.CollisionEnergy)

	@property
	def fragmentor_voltage(self) -> float:
		"""
		Returns the value of the Fragmentor Voltage used to acquire the data.
		"""

		# Also float(self.data_reader.MSOverallScanRecordInformation.FragmentorVoltage)
		return float(self.interface.FragmentorVoltage)  # volts

	@property
	def ionization_polarity(self) -> Optional[str]:
		"""
		Returns the ionization polarity used to acquire the data.
		"""

		return polarity_map[self.interface.IonPolarity]

	@property
	def ionization_mode(self) -> IonizationMode:
		"""
		Returns the ionization mode used to acquire the data.
		"""

		# Also IonizationMode(dr.get_tic().data_reader.MSOverallScanRecordInformation.IonizationMode)
		return IonizationMode(self.interface.IonizationMode)

	@property
	def ms_level(self) -> MSLevel:
		"""
		Returns the mass spectrometry level, if the data was obtained via mass spectrometry.
		"""

		# Also MSLevel(self.data_reader.MSOverallScanRecordInformation.MSLevel)
		return MSLevel(self.interface.MSLevelInfo)

	@property
	def ms_scan_type(self) -> MSScanType:
		"""
		Returns the mass spectrometry scan type, if the data was obtained via mass spectrometry.
		"""

		# Also MSScanType(dr.get_tic().data_reader.MSOverallScanRecordInformation.MSScanType)
		return MSScanType(self.interface.MSScanType)

	@property
	def ms_storage_mode(self) -> MSStorageMode:
		"""
		Returns the storage mode of the mass spectrometry data, if the data was obtained via mass spectrometry.
		"""

		return MSStorageMode(self.interface.MSStorageMode)

	@property
	def mz_of_interest(self) -> List[Range]:
		r"""
		Returns a list of |mz| ranges of interest, if the data was obtained via mass spectrometry.

		For MS\ :superscript:`1` data this is not used.

		.. TODO:: revisit with ms/ms data
		"""  # noqa RST305

		return ranges_from_list(self.interface.MZOfInterest)

	@property
	def measured_mass_range(self) -> List[Range]:
		"""
		Returns the measured |mz| range(s), if the data was obtained via mass spectrometry.
		"""  # noqa RST305

		return ranges_from_list(self.interface.MeasuredMassRange)

	@property
	def mz_regions_were_excluded(self) -> bool:
		"""
		Returns whether any |mz| ranges were excluded, if the data was obtained via mass spectrometry.
		"""  # noqa RST305

		# TODO: excluded from what? the scan?
		return bool(self.interface.MzRegionsWereExcluded)

	@property
	def sampling_period(self) -> float:
		"""
		Return the sampling period (the inter-scan delay) for the data.
		"""

		return float(self.interface.SamplingPeriod)  # interscan delay? 0.5 would be 2 scan / second

	@property
	def threshold(self) -> float:
		"""
		Returns the threshold of the data.

		.. TODO:: What does this represent?
		"""

		return float(self.interface.Threshold)

	def get_x_axis_info(self) -> Tuple[DataValueType, DataUnit]:
		"""
		Returns the type of data represented by the x-axis, and the corresponding unit.
		"""

		_, unit, value_type = self.interface.GetXAxisInfoChrom(0, 0)
		return DataValueType(value_type), DataUnit(unit)

	def get_y_axis_info(self) -> Tuple[DataValueType, DataUnit]:
		"""
		Returns the type of data represented by the y-axis, and the corresponding unit.
		"""

		_, unit, value_type = self.interface.GetYAxisInfoChrom(0, 0)
		return DataValueType(value_type), DataUnit(unit)


# TODO: frozen TIC

#  ChromFilter
#  CreateBDAChromData
#  GetHashCode
#  GetType
#  GetXAxisInfo  # seems to be the same as GetXAxisChromInfo - perhaps used for non-chrom?
#  GetYAxisInfo  # seems to be the same as GetYAxisChromInfo - perhaps used for non-chrom?
#  ReferenceEquals ?
#  Smooth  # manipulates
#  TrimXRange  # manipulates

#  XSpecificData  # but is None?
#  DeviceIDInfo -> int
#  MSOverallScanRecordInformation -> Agilent.MassSpectrometry.DataAnalysis.MSOverallScanRecordInfo
#  MeasuredMassRangeInfo -> Agilent.MassSpectrometry.DataAnalysis.BDARangeCollection

# MeasuredMassRangeInfo
# ----
# Capacity
# Count
# GetEnumerator
# GetHashCode
# GetType
# InnerList
# IsEmpty
# List
# Remove
# RemoveAt
# Reverse
# SetEmpty
# Sort
