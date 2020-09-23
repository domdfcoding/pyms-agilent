#  !/usr/bin/env python
#
#  file_information.py
"""
Provides metadata about ``.d`` datafiles.
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
from datetime import datetime, timezone
from typing import Union

# this package
from pyms_agilent.enums import DeviceType, IRMStatus, MeasurementTypeEnum, SeparationTechniqueEnum, StoredDataType
from pyms_agilent.mhdac.agilent import DataAnalysis
from pyms_agilent.mhdac.ms_scan_file_info import MSScanFileInformation

__all__ = ["FileInformation"]


class FileInformation:
	"""
	Class to access information about ``.d`` data files.

	:param data_reader: Python.NET object.
	"""

	#: The .NET interface
	interface: DataAnalysis.IBDAFileInformation

	#: The .NET class that provides access to the data.
	data_reader: Union[DataAnalysis.BDAFileInformation, DataAnalysis.BDAMSScanFileInformation]

	def __init__(self, data_reader: Union[DataAnalysis.BDAFileInformation, DataAnalysis.BDAMSScanFileInformation]):

		self.data_reader = data_reader
		self.interface = DataAnalysis.IBDAFileInformation(self.data_reader)

	@property
	def acquisition_time(self) -> datetime:
		"""
		Returns the acquisition time of the data, as a string.

		.. TODO:: See if the time reflects the system time, or is always UTC.
		"""

		acq_time = self.interface.AcquisitionTime

		return datetime(
				year=acq_time.Year,
				month=acq_time.Month,
				day=acq_time.Day,
				hour=acq_time.Hour,
				minute=acq_time.Minute,
				second=acq_time.Second,
				tzinfo=timezone.utc,
				)

	@property
	def irm_status(self) -> IRMStatus:
		"""
		Returns the IRM/Runtime calibration status information - success or failure.

		This is the logical bitwise OR of the IRMStatusValues of the IRM status for all scans in the file.
		"""

		return IRMStatus(self.interface.IRMStatus)

	@property
	def datafile_name(self) -> str:
		"""
		Returns the name of the data file.
		"""

		return self.interface.DataFileName

	@property
	def ms_data_present(self) -> bool:
		"""
		Returns whether mass spectrometry data is present in the datafile.

		:return:
		"""

		return self.interface.IsMSDataPresent()

	@property
	def non_ms_data_present(self) -> bool:
		"""
		Returns whether non-mass spectrometry data is present in the datafile,
		with the exception UV spectral data.
		"""  # noqa D400

		return self.interface.IsNonMSDataPresent()

	@property
	def uv_data_present(self) -> bool:
		"""
		Returns whether UV spectral data is present in the datafile.
		"""

		return self.interface.IsUVSpectralDataPresent()

	@property
	def measurement_type(self) -> MeasurementTypeEnum:
		"""
		Returns the measurement mode information, e.g. chromatographic or direct infusion.
		"""

		return MeasurementTypeEnum(self.interface.MeasurementType)

	@property
	def separation_technique(self) -> SeparationTechniqueEnum:
		"""
		Returns the separation technique information, e.g. GC, LC, CE.
		"""

		return SeparationTechniqueEnum(self.interface.SeparationTechnique)

	@property
	def ms_scan_file_info(self) -> MSScanFileInformation:
		"""
		Returns a class containing information about the MS Scan File.
		"""

		return MSScanFileInformation(self.interface.MSScanFileInformation)

	def is_uv_signal_present(self, device_type: DeviceType, signal_name: str, device_name: str):
		"""
		Returns whether a UV signal is present for the specified device type.

		:param device_type: The type of device that acquired the data.
		:param signal_name:
		:param device_name: The name of the device that acquired the data.

		.. TODO:: Look in MassHunter at signal names
		"""

		# TODO: see why the [0] is needed
		return self.interface.IsUVSignalPresent(device_type, signal_name, device_name)[0]

	def is_datatype_present(self, datatype: StoredDataType, device_name: str, ordinal_number: int = 1) -> bool:
		"""
		Returns whether data is present for the given device.

		:param datatype: The type of data to check for.
		:param device_name: The name of the device.
		:param ordinal_number: The ordinal number of the device.
		"""

		return self.interface.IsStoredDataTypePresent(f"{device_name}{ordinal_number}", datatype)

	def get_device_name(self, device_type: DeviceType) -> str:
		"""
		Returns the name of the device in the instrument configuration with the given type.

		:param device_type:
		"""

		return self.interface.GetDeviceName(device_type)


# data reader
# ----
# Close
# CombineFileInformation
# Equals
# Finalize
# GetHashCode
# GetType
# MemberwiseClone
# Overloads
# ReferenceEquals

# Interface
# -----------
# Clear
# Clone
# GetDeviceTable  # broken
# GetSignalTable  # broken
# GetSpectrumXAxisLimit  # broken
