#  !/usr/bin/env python
#
#  spectrum.py
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
from typing import List, Optional, Tuple

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
from pyms_agilent.utils import Range, polarity_map, ranges_from_list

__all__ = ["SpecData"]


class SpecData:
	"""
	Class to access information about a single spectrum in ``.d`` data files.

	:param BDASpecData: Python.NET object.
	"""

	def __init__(self, BDASpecData: DataAnalysis.BDASpecData):
		self.data_reader = BDASpecData
		self.interface = DataAnalysis.IBDASpecData(self.data_reader)

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

		"""

		return int(self.interface.ChromPeakIndex)

	@property
	def collision_energy(self) -> float:
		"""
		Returns the collision energy used to acquire the data.
		"""

		return float(self.interface.CollisionEnergy)

	def compensation_field(self) -> float:
		"""

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

	def dispersion_field(self) -> float:
		"""

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
			acquired in MS\ :superscript:`2` mode
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
	# 	Returns the *m/z* of interest.
	#
	# 	*m/z* of interest takes on a different meaning depending on the scan type:
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
		Returns a list of *m/z* ranges of interest, if the data was obtained via mass spectrometry.

		For MS\ :superscript:`1` data this is not used.

		TODO: revisit with ms/ms data
		"""

		return ranges_from_list(self.interface.MZOfInterest)

	@property
	def measured_mass_range(self) -> List[Range]:
		"""
		Returns the measured *m/z* range(s), if the data was obtained via mass spectrometry.
		"""

		return Range.from_dotnet(self.interface.MeasuredMassRange)

	@property
	def ordinal_number(self) -> int:
		"""

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
