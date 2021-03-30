#  !/usr/bin/env python
#
#  spectrum.py
"""
Provides access to information about a single spectrum in ``.d`` data files.
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
#  pretty_frozen_spec_data based on https://github.com/tommikaikkonen/prettyprinter
#  Copyright (c) 2017, Tommi Kaikkonen
#  MIT Licensed
#  |  Permission is hereby granted, free of charge, to any person obtaining a copy
#  |  of this software and associated documentation files (the "Software"), to deal
#  |  in the Software without restriction, including without limitation the rights
#  |  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  |  copies of the Software, and to permit persons to whom the Software is
#  |  furnished to do so, subject to the following conditions:
#  |
#  |  The above copyright notice and this permission notice shall be included in all
#  |  copies or substantial portions of the Software.
#  |
#  |  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  |  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  |  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  |  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  |  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  |  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  |  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import Any, Iterable, List, MutableMapping, Optional, Tuple

# 3rd party
import attr
import prettyprinter  # type: ignore
from attr_utils.pprinter import pretty_repr, register_pretty
from attr_utils.serialise import serde
from domdf_python_tools.utils import etc
from prettyprinter import pretty_call_alt

# this package
from pyms_agilent.enums import (
		DataUnit,
		DataValueType,
		DeviceType,
		IonizationMode,
		MSLevel,
		MSScanType,
		MSStorageMode,
		SpecType
		)
from pyms_agilent.exceptions import NotMS2Error
from pyms_agilent.mhdac.agilent import DataAnalysis
from pyms_agilent.mhdac.chromatograms import axis_info_converter
from pyms_agilent.utils import Range, frozen_comparison, polarity_map, ranges_from_list

__all__ = [
		"SpecData",
		"FrozenSpecData",
		"FrozenMS2SpecData",
		"pretty_etc",
		"pretty_frozen_spec_data",
		"pretty_spec_data",
		]


class SpecData:  # pragma: no cover (!Windows)
	"""
	Class to access information about a single spectrum in ``.d`` data files.

	:param BDASpecData: Python.NET object.
	"""

	def __init__(self, BDASpecData: "DataAnalysis.BDASpecData"):
		self.data_reader = BDASpecData
		self.interface: DataAnalysis.IBDASpecData = DataAnalysis.IBDASpecData(self.data_reader)

	@property
	def abundance_limit(self) -> float:
		"""
		Returns the abundance limit of the spectral data; that is the largest value that could be seen
		in the spectrum (the theoretical "full scale" value).
		"""  # noqa D400

		return float(self.interface.AbundanceLimit)

	@property
	def acquired_time_ranges(self) -> List[Range]:
		"""
		Returns the list of time ranges over which the data was acquired.

		If the data was acquired over only one time range, the list will contain only one element.
		"""

		return ranges_from_list(self.interface.AcquiredTimeRange)

	@property
	def chrom_peak_index(self) -> int:
		"""
		.. TODO:: What does this represent?
		"""

		return int(self.interface.ChromPeakIndex)

	@property
	def collision_energy(self) -> float:
		"""
		Returns the collision energy used to acquire the data.
		"""

		return float(self.interface.CollisionEnergy)

	@property
	def compensation_field(self) -> float:
		"""
		Returns the value of the compensation field.
		"""

		return float(self.interface.CompensationField)

	# @property
	# def convert_data_to_mass_units(self):
	# 	"""
	#
	# 	"""
	#
	# 	return self.interface.ConvertDataToMassUnits # TODO

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
	def dispersion_field(self) -> float:
		"""
		Returns the value of the dispersion field.
		"""

		return float(self.interface.DispersionField)

	@property
	def fragmentor_voltage(self) -> float:
		"""
		Returns the value of the Fragmentor Voltage used to acquire the data.
		"""

		return float(self.interface.FragmentorVoltage)

	@property
	def precursor_charge(self) -> int:
		r"""
		Returns the charge of the precursor ion, if the data was acquired in MS\ :superscript:`2` mode.

		:raises: :exc:`pyms_agilent.errors.NotMS2Error` if the data was not
			acquired in MS\ :superscript:`2` mode.
		"""

		is_ms2: bool
		charge: int

		is_ms2, charge = self.interface.GetPrecursorCharge(0)

		if not is_ms2:
			raise NotMS2Error()
		else:
			return int(charge)

	@property
	def precursor_intensity(self) -> float:
		r"""
		Returns the intensity of the precursor ion, if the data was acquired in MS\ :superscript:`2` mode.

		:raises: :exc:`pyms_agilent.errors.NotMS2Error` if the data was not
			acquired in MS\ :superscript:`2` mode
		"""

		is_ms2: bool
		charge: int

		is_ms2, intensity = self.interface.GetPrecursorIntensity(0)

		if not is_ms2:
			raise NotMS2Error()
		else:
			return float(intensity)

	#
	# @property
	# def mz_of_interest(self) -> float:
	# 	"""
	# 	Returns the |mz| of interest.
	#
	# 	|mz| of interest takes on a different meaning depending on the scan type:
	#
	# 	* MS scans (scan, selected ion, high resolution scan) do not have m/z of interest.
	# 	* MRM: precursor mass
	# 	* Product ion: precursor mass
	# 	* Precursor ion: product ion mass
	# 	* Neutral loss: loss mass
	# 	* Neutral gain: gain mass
	#
	# 	:raises: :exc:`pyms_agilent.errors.NotMS2Error` if the data was not
	# 		acquired in MS\ :superscript:`2` mode
	#
	# 	.. TODO:: revisit with MS/MS data
	# 	"""
	#
	# 	# TODO:
	# 	ions, count = self.interface.GetPrecursorIntensity(0)

	def get_x_axis_info(self) -> Tuple[DataValueType, DataUnit]:
		"""
		Returns the type of data represented by the x-axis, and the corresponding unit.
		"""

		_, unit, value_type = self.interface.GetXAxisInfoSpec(0, 0)
		return DataValueType(value_type), DataUnit(unit)

	def get_y_axis_info(self) -> Tuple[DataValueType, DataUnit]:
		"""
		Returns the type of data represented by the y-axis, and the corresponding unit.
		"""

		_, unit, value_type = self.interface.GetYAxisInfoSpec(0, 0)
		return DataValueType(value_type), DataUnit(unit)

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

		return IonizationMode(self.interface.IonizationMode)

	@property
	def is_chromatogram(self) -> bool:
		"""
		Returns whether the data is a chromatogram.
		"""

		return bool(self.interface.IsChromatogram)

	@property
	def is_data_in_mass_unit(self) -> bool:
		"""
		Returns whether the x-axis data is in mass units.
		"""

		return bool(self.interface.IsDataInMassUnit)

	@property
	def is_mass_spectrum(self) -> bool:
		"""
		Returns whether the data is a mass spectrum.
		"""

		return bool(self.interface.IsMassSpectrum)

	@property
	def is_icp_data(self) -> bool:
		"""
		Returns whether the data is ICP (inductively coupled plasma) data.
		"""

		return self.data_reader.IsICPData

	@property
	def is_uv_spectrum(self) -> bool:
		"""
		Returns whether the data is a UV-Vis spectrum.
		"""

		return bool(self.interface.IsUvSpectrum)

	@property
	def ms_level(self) -> MSLevel:
		"""
		Returns the mass spectrometry level, if the data was obtained via mass spectrometry.
		"""

		return MSLevel(self.interface.MSLevelInfo)

	@property
	def ms_scan_type(self) -> MSScanType:
		"""
		Returns the mass spectrometry scan type, if the data was obtained via mass spectrometry.
		"""

		return MSScanType(self.interface.MSScanType)

	@property
	def ms_storage_mode(self) -> MSStorageMode:
		"""
		Returns the storage mode of the mass spectrometry data, if the data was obtained via mass spectrometry.
		"""

		# Also MSStorageMode(spec.data_reader.StorageMode)
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
	def measured_mass_range(self) -> Optional[Range]:
		"""
		Returns the measured |mz| range, if the data was obtained via mass spectrometry.
		"""  # noqa RST305

		_range = self.interface.MeasuredMassRange
		if _range is not None:
			return Range.from_dotnet(_range)
		return None

	@property
	def ordinal_number(self) -> int:
		"""
		Returns the ordinal number of the spectrum.
		"""

		return int(self.interface.OrdinalNumber)

	@property
	def parent_scan_id(self) -> int:
		"""
		Returns the ID number of the parent scan, if applicable.

		If there is no parent scan ``0`` is returned.
		"""

		return int(self.interface.ParentScanId)

	@property
	def sampling_period(self) -> float:
		"""
		Returns the sampling period (the inter-scan delay) for the data.
		"""

		return float(self.interface.SamplingPeriod)

	# def scaleYValues(self):
	# 	return self.interface.ScaleYValues  # TODO

	@property
	def scan_id(self) -> int:
		"""
		Returns the ID of the scan.

		If this spectrum is the result of several scans (e.g. an averaged spectrum)
		the scan ID will be ``0``.
		"""

		return int(self.interface.ScanId)

	# def specFilter(self):
	# 	return self.interface.SpecFilter  # TODO

	@property
	def spectrum_type(self) -> SpecType:
		"""
		Returns the type of spectrum.
		"""

		# Also SpecType(spec.data_reader.SpectrumTypeInfo))
		return SpecType(self.interface.SpectrumType)

	@property
	def threshold(self) -> float:
		"""
		.. TODO:: What does this represent?
		"""

		return float(self.interface.Threshold)

	# def tofCalibration(self):
	# 	return self.interface.TofCalibration  # TODO

	@property
	def total_data_points(self) -> int:
		"""
		Returns the total number of data points.
		"""

		return int(self.interface.TotalDataPoints)

	@property
	def total_scan_count(self) -> int:
		"""
		Returns the total number of scans that made up this spectrum.
		"""

		return int(self.interface.TotalScanCount)

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

	# @property
	# def scan_time(self) -> float:
	# 	"""
	# 	Returns time the scan was acquired at
	# 	"""
	#
	# 	return self.acquired_time_ranges[0].start

	def __repr__(self) -> str:
		"""
		Return a string representation of the :class:`~.SpecData`.
		"""

		return prettyprinter.pformat(self)

	def to_dict(self) -> MutableMapping[str, Any]:
		"""
		Returns a dictionary containing the data of this
		:class:`~pyms_agilent.mhdac.spectrum.SpecData` object.
		"""  # noqa: D400

		the_dict = dict(
				abundance_limit=self.abundance_limit,
				acquired_time_ranges=self.acquired_time_ranges,
				chrom_peak_index=self.chrom_peak_index,
				collision_energy=self.collision_energy,
				compensation_field=self.compensation_field,
				device_name=self.device_name,
				device_type=self.device_type,
				dispersion_field=self.dispersion_field,
				fragmentor_voltage=self.fragmentor_voltage,
				x_axis_info=self.get_x_axis_info(),
				y_axis_info=self.get_y_axis_info(),
				ionization_polarity=self.ionization_polarity,
				ionization_mode=self.ionization_mode,
				is_chromatogram=self.is_chromatogram,
				is_data_in_mass_unit=self.is_data_in_mass_unit,
				is_mass_spectrum=self.is_mass_spectrum,
				is_icp_data=self.is_icp_data,
				is_uv_spectrum=self.is_uv_spectrum,
				ms_level=self.ms_level,
				ms_scan_type=self.ms_scan_type,
				ms_storage_mode=self.ms_storage_mode,
				mz_of_interest=self.mz_of_interest,
				measured_mass_range=self.measured_mass_range,
				ordinal_number=self.ordinal_number,
				parent_scan_id=self.parent_scan_id,
				sampling_period=self.sampling_period,
				scan_id=self.scan_id,
				spectrum_type=self.spectrum_type,
				threshold=self.threshold,
				total_data_points=self.total_data_points,
				total_scan_count=self.total_scan_count,
				x_data=self.x_data,
				y_data=self.y_data,
				)

		if self.ms_level == MSLevel.MSMS:
			the_dict["precursor_charge"] = self.precursor_charge
			the_dict["precursor_intensity"] = self.precursor_intensity

		return the_dict

	def freeze(self) -> "FrozenSpecData":
		"""
		Returns a :class:`~pyms_agilent.mhdac.spectrum.FrozenSpecData` object
		containing the same data as this object.
		"""  # noqa: D400

		if self.ms_level == MSLevel.MSMS:
			return FrozenMS2SpecData(**self.to_dict())

		else:
			return FrozenSpecData(**self.to_dict())


# data_reader
# ===============
# AcquiredTimeRangesInfo
# Calibration
# DeviceIDInfo
# FileXSamplingType
# FilteredScanCountInfo
# GetPointDataValueTypeForIndex
# IsDeviceOfTypeTOF
# IsEmptySpectrumInfo
# IsNullMSSpectrumFormat
# MSOverallScanRecordInformation -> Contains some more properties
# MSSpectrumFormatXSamplingType
# MeasuredMassRangeInfo
# OverallAcqTimeRangeInfo # No idea; different from AcquiredTimeRange
# SelectedIonsInfo
# XSpecificData

# interface
# ==========
# ScaleYValues
# SpecFilter
# TofCalibration
# ConvertDataToMassUnits  # Converts the spectrum to mass units if it is in time units. Presumably mutates data?


def _range_converter(iterable: Iterable[Range]) -> List[Range]:
	return list(iterable)


@serde
@pretty_repr
@frozen_comparison(SpecData)
@attr.s(slots=True, frozen=True, eq=False, repr=False)
class FrozenSpecData:
	"""
	Frozen version of :class:`~.SpecData`.

	Provides metadata about a single spectrum.
	"""

	abundance_limit: float = attr.ib(converter=float)
	"""
	The abundance limit of the spectral data; that is the largest value that could be seen
	in the spectrum (the theoretical "full scale" value).
	"""

	acquired_time_ranges: List[Range] = attr.ib(converter=_range_converter)
	"""
	The list of time ranges over which the data was acquired.

	If the data was acquired over only one time range, the list will contain only one element.
	"""

	#: The collision energy used to acquire the data.
	chrom_peak_index: int = attr.ib(converter=int)

	#: The value of the compensation field.
	collision_energy: float = attr.ib(converter=float)

	#: The name of the device used to acquire the data.
	compensation_field: float = attr.ib(converter=float)

	#: The type of device used to acquire the data.
	device_name: str = attr.ib(converter=str)

	#: The value of the dispersion field.
	device_type: DeviceType = attr.ib(converter=DeviceType)

	#: The value of the Fragmentor Voltage used to acquire the data.
	dispersion_field: float = attr.ib(converter=float)

	#: The value of the Fragmentor Voltage used to acquire the data.
	fragmentor_voltage: float = attr.ib(converter=float)

	#: The type of data represented by the x-axis, and the corresponding unit.
	x_axis_info: Tuple[DataValueType, DataUnit] = attr.ib(converter=axis_info_converter)

	#: The type of data represented by the y-axis, and the corresponding unit.
	y_axis_info: Tuple[DataValueType, DataUnit] = attr.ib(converter=axis_info_converter)

	#: The ionization polarity used to acquire the data.
	ionization_polarity: Optional[str] = attr.ib()

	#: The ionization mode used to acquire the data.
	ionization_mode: IonizationMode = attr.ib(converter=IonizationMode)

	#: Whether the data is a chromatogram.
	is_chromatogram: bool = attr.ib(converter=bool)

	#: Whether the x-axis data is in mass units.
	is_data_in_mass_unit: bool = attr.ib(converter=bool)

	#: Wether the data is a mass spectrum.
	is_mass_spectrum: bool = attr.ib(converter=bool)

	#: Wether the data is ICP (inductively coupled plasma) data.
	is_icp_data: bool = attr.ib(converter=bool)

	#: Whether the data is a UV-Vis spectrum.
	is_uv_spectrum: bool = attr.ib(converter=bool)

	#: The mass spectrometry level, if the data was obtained via mass spectrometry.
	ms_level: MSLevel = attr.ib(converter=MSLevel)

	#: The mass spectrometry scan type, if the data was obtained via mass spectrometry.
	ms_scan_type: MSScanType = attr.ib(converter=MSScanType)

	#: The storage mode of the mass spectrometry data, if the data was obtained via mass spectrometry.
	ms_storage_mode: MSStorageMode = attr.ib(converter=MSStorageMode)

	mz_of_interest: List[Range] = attr.ib(converter=_range_converter)
	r"""
	A list of |mz| ranges of interest, if the data was obtained via mass spectrometry.

	For MS\ :superscript:`1` data this is not used.
	"""

	#: The measured |mz| range(s), if the data was obtained via mass spectrometry.
	measured_mass_range: Range = attr.ib()

	#: The ordinal number of the spectrum.
	ordinal_number: int = attr.ib(converter=int)

	parent_scan_id: int = attr.ib(converter=int)
	"""
	The ID number of the parent scan, if applicable.

	If there is no parent scan ``0`` is returned.
	"""

	#: The sampling period (the inter-scan delay) for the data.
	sampling_period: float = attr.ib(converter=float)

	scan_id: int = attr.ib(converter=int)
	"""
	The ID of the scan.

	If this spectrum is the result of several scans (e.g. an averaged spectrum)
	the scan ID will be ``0``.
	"""

	#: The type of spectrum.
	spectrum_type: SpecType = attr.ib(converter=SpecType)

	threshold: float = attr.ib(converter=float)

	#: The total number of data points.
	total_data_points: int = attr.ib(converter=int)

	#: The total number of scans that made up this spectrum.
	total_scan_count: int = attr.ib(converter=int)

	#: The x-axis data.
	x_data: List[float] = attr.ib(converter=list)

	#: The y-axis data.
	y_data: List[float] = attr.ib(converter=list)

	def get_x_axis_info(self) -> Tuple[DataValueType, DataUnit]:
		"""
		Returns the type of data represented by the x-axis, and the corresponding unit.
		"""

		return self.x_axis_info

	def get_y_axis_info(self) -> Tuple[DataValueType, DataUnit]:
		"""
		Returns the type of data represented by the y-axis, and the corresponding unit.
		"""

		return self.y_axis_info

	@property
	def precursor_charge(self) -> int:
		r"""
		The charge of the precursor ion, if the data was acquired in MS\ :superscript:`2` mode.

		Raises an :exc:`pyms_agilent.errors.NotMS2Error` if the data was not
		acquired in MS\ :superscript:`2` mode.
		"""

		raise NotMS2Error()

	@property
	def precursor_intensity(self) -> float:
		r"""
		The intensity of the precursor ion, if the data was acquired in MS\ :superscript:`2` mode.

		Raises an :exc:`pyms_agilent.errors.NotMS2Error` if the data was not
		acquired in MS\ :superscript:`2` mode.
		"""

		raise NotMS2Error()


@attr.s(slots=True, frozen=True, eq=False)
class FrozenMS2SpecData(FrozenSpecData):
	r"""
	Frozen version of :class:`~.SpecData` for MS\ :superscript:`2` data.

	Provides metadata about a single spectrum.
	"""

	precursor_charge: int = attr.ib(converter=int)
	r"""
	The charge of the precursor ion, if the data was acquired in MS\ :superscript:`2` mode.

	Raises an :exc:`pyms_agilent.errors.NotMS2Error` if the data was not
	acquired in MS\ :superscript:`2` mode.
	"""

	precursor_intensity: float = attr.ib(converter=float)
	r"""
	The intensity of the precursor ion, if the data was acquired in MS\ :superscript:`2` mode.

	Raises an :exc:`pyms_agilent.errors.NotMS2Error` if the data was not
	acquired in MS\ :superscript:`2` mode.
	"""


# has to be done after FrozenSpecData was defined.
frozen_comparison(FrozenSpecData)(SpecData)


@register_pretty(type(etc))
def pretty_etc(value, ctx):  # noqa: D103
	return repr(value)


@register_pretty(FrozenSpecData)
def pretty_frozen_spec_data(value, ctx):
	"""
	PrettyPrinter for :class:``~.FrozenSpecData``.
	"""

	cls = type(value)
	attributes = cls.__attrs_attrs__

	kwargs = []
	for attribute in attributes:
		if not attribute.repr:
			continue

		display_attr = False
		if attribute.default == attr.NOTHING:
			display_attr = True
		elif isinstance(attribute.default, attr.Factory):  # type: ignore
			default_value = (
					attribute.default.factory(value)
					if attribute.default.takes_self else attribute.default.factory()
					)
			if default_value != getattr(value, attribute.name):
				display_attr = True
		else:
			if attribute.default != getattr(value, attribute.name):
				display_attr = True

		if display_attr:
			if attribute.name in {"x_data", "y_data"}:
				kwargs.append((attribute.name, [*getattr(value, attribute.name)[:10], etc]))
			else:
				kwargs.append((attribute.name, getattr(value, attribute.name)))

	return pretty_call_alt(ctx, cls, kwargs=kwargs)


@register_pretty(SpecData)
def pretty_spec_data(value, ctx):  # pragma: no cover (!Windows)
	"""
	PrettyPrinter for :class:``~.SpecData``.
	"""

	cls = type(value)
	kwargs = []

	for key, value in value.to_dict().items():
		if key in {"x_data", "y_data"}:
			kwargs.append((key, [*value[:10], etc]))
		else:
			kwargs.append((key, value))

	return pretty_call_alt(ctx, cls, kwargs=kwargs)
