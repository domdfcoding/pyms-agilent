#  !/usr/bin/env python
#
#  data_reader.py
"""
Higher level interface for reading ``.d`` data files..
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
from datetime import datetime
from typing import Any, Dict, List, Optional

# 3rd party
from domdf_python_tools.typing import PathLike
from memoized_property import memoized_property

# this package
from pyms_agilent.enums import (
		DeviceType,
		IonizationMode,
		IRMStatus,
		MeasurementTypeEnum,
		MSScanType,
		MSStorageMode,
		SampleCategory,
		SeparationTechniqueEnum,
		StoredDataType
		)
from pyms_agilent.mhdac import mass_spec_data_reader
from pyms_agilent.mhdac.chromatograms import TIC
from pyms_agilent.mhdac.file_information import FileInformation
from pyms_agilent.mhdac.mass_spec_data_reader import MSActuals
from pyms_agilent.mhdac.ms_scan_file_info import MSScanFileInformation
from pyms_agilent.mhdac.scan_record import MSScanRecord
from pyms_agilent.mhdac.signalinfo import SignalInfo
from pyms_agilent.mhdac.spectrum import SpecData

__all__ = ["DataReader"]


class DataReader:
	"""
	The primary interface for reading data files.

	This class combined information from three nested classes in
	:mod:`pyms_agilent.mhdac` into one.

	:param filename: The ``.d`` data file to open.
	"""

	def __init__(self, filename: PathLike):
		self.filename: str = str(filename)

		# The lower level class we wrap
		self._data_reader = mass_spec_data_reader.MassSpecDataReader(filename)

	def close_datafile(self) -> bool:
		"""
		Closes the datafile.

		:return:
		"""

		return self._data_reader.close_datafile()

	def __del__(self):
		self.close_datafile()

	def refresh_datafile(self) -> bool:
		"""
		Refreshes the data file and returns whether new data is present.

		:return: Whether new data is present in the data file
		"""

		return self._data_reader.refresh_datafile()

	# TODO: file_information

	_file_info: FileInformation
	_ms_scan_file_info: MSScanFileInformation

	@memoized_property
	def _file_info(self) -> FileInformation:
		return self._data_reader.file_information

	@memoized_property
	def _ms_scan_file_info(self) -> MSScanFileInformation:
		return self._file_info.ms_scan_file_info

	@property
	def acquisition_time(self) -> datetime:
		"""
		Returns the acquisition time of the data, as a string.
		"""

		return self._file_info.acquisition_time

	@property
	def irm_status(self) -> IRMStatus:
		"""
		Returns the IRM/Runtime calibration status information - success or failure.

		This is the logical bitwise OR of the IRMStatusValues of the IRM status for all scans in the file.
		"""

		return self._file_info.irm_status

	@property
	def datafile_name(self) -> str:
		"""
		Returns the name of the data file.
		"""

		return self._file_info.datafile_name

	@property
	def ms_data_present(self) -> bool:
		"""
		Returns whether mass spectrometry data is present in the datafile.

		:return:
		"""

		return self._file_info.ms_data_present

	@property
	def non_ms_data_present(self) -> bool:
		"""
		Returns whether non-mass spectrometry data is present in the datafile,
		with the exception UV spectral data.
		"""  # noqa D400

		return self._file_info.non_ms_data_present

	@property
	def uv_data_present(self) -> bool:
		"""
		Returns whether UV spectral data is present in the datafile.
		"""

		return self._file_info.uv_data_present

	@property
	def measurement_type(self) -> MeasurementTypeEnum:
		"""
		Returns the measurement mode information, e.g. chromatographic or direct infusion.
		"""

		return self._file_info.measurement_type

	@property
	def separation_technique(self) -> SeparationTechniqueEnum:
		"""
		Returns the separation technique information, e.g. GC, LC, CE.
		"""

		return self._file_info.separation_technique

	@property
	def collision_energies(self) -> List[float]:
		"""
		Returns the collision energies used to acquire the data.
		"""

		return self._ms_scan_file_info.collision_energies

	@property
	def compensation_field_values(self) -> List[float]:
		"""
		Returns the compensation field values.
		"""

		return self._ms_scan_file_info.compensation_field_values

	@property
	def dispersion_field_values(self) -> List[float]:
		"""
		Returns the dispersion field values.
		"""

		return self._ms_scan_file_info.dispersion_field_values

	@property
	def has_ms_data(self) -> bool:
		"""
		Returns whether the file contains mass spectral data.
		"""

		return self._ms_scan_file_info.has_ms_data

	@property
	def device_type(self) -> DeviceType:
		"""
		Returns the type of device used to acquire the data.
		"""

		return self._ms_scan_file_info.device_type

	@property
	def fragmentor_voltages(self) -> List[float]:
		"""
		Returns the fragmentor voltages used to acquire the data.
		"""

		return self._ms_scan_file_info.fragmentor_voltages

	@property
	def ionisation_mode(self) -> IonizationMode:
		"""
		Returns the ionization mode used to acquire the data.

		This is the logical bitwise OR of the Ionization Mode values for all scans in the file
		"""

		return self._ms_scan_file_info.ionisation_mode

	@property
	def ionisation_polarity(self) -> Optional[str]:
		"""
		Returns the ionization polarity used to acquire the data.
		"""

		return self._ms_scan_file_info.ionisation_polarity

	@property
	def ms_level(self) -> int:
		"""
		Returns the MS level used to acquire the data.
		"""

		return self._ms_scan_file_info.ms_level

	@property
	def scan_types(self) -> MSScanType:
		"""
		Returns the MS Scan Type.

		This is the logical bitwise OR of the MSScanType values for all scans in the file.
		"""

		return self._ms_scan_file_info.scan_types

	@property
	def spectra_format(self) -> MSStorageMode:
		"""
		Returns the format of the spectrum.
		"""

		return self._ms_scan_file_info.spectra_format

	@property
	def total_scans(self) -> int:
		"""
		Returns the total number of scans present.
		"""

		return self._ms_scan_file_info.total_scans

	@property
	def has_fixed_cycle_length_data(self) -> bool:
		"""
		Returns whether the data file contains any time segments that have a fixed cycle length.
		"""

		return self._ms_scan_file_info.has_fixed_cycle_length_data

	@property
	def are_multiple_spectra_present_per_scan(self) -> bool:
		"""
		Returns whether the data file contains more than 1 spectra format for each scan.

		This is useful in case of dual mode format stored for each scan.
		"""

		return self._ms_scan_file_info.are_multiple_spectra_present_per_scan

	@property
	def sim_ions(self) -> List[float]:
		"""
		Returns a list of SIM ions.
		"""

		return self._ms_scan_file_info.sim_ions

	def is_uv_signal_present(self, device_type: DeviceType, signal_name: str, device_name: str):
		"""
		Returns whether a UV signal is present for the specified device type.

		:param device_type: The type of device that acquired the data.
		:param signal_name:
		:param device_name: The name of the device that acquired the data.
		"""

		return self._file_info.is_uv_signal_present(
				device_type=device_type,
				signal_name=signal_name,
				device_name=device_name,
				)

	def is_datatype_present(self, datatype: StoredDataType, device_name: str, ordinal_number: int = 1) -> bool:
		"""
		Returns whether data is present for the given device.

		:param datatype: The type of data to check for.
		:param device_name: The name of the device.
		:param ordinal_number: The ordinal number of the device.
		"""

		return self._file_info.is_datatype_present(
				datatype=datatype,
				device_name=device_name,
				ordinal_number=ordinal_number,
				)

	def get_device_name(self, device_type: DeviceType) -> str:
		"""
		Returns the name of the device in the instrument configuration with the given type.

		:param device_type:
		"""

		return self._file_info.get_device_name(device_type)

	def get_tic(self) -> TIC:
		"""
		Returns the total ion chromatogram of the data.
		"""

		return self._data_reader.get_tic()

	def get_spectrum_by_scan(self, scan_no: int) -> SpecData:
		"""
		Returns a :class:`pyms_agilent.mhdac.spectrum.SpecData` object for the given scan.

		:param scan_no:
		"""

		return self._data_reader.get_spectrum_by_scan(scan_no)

	def get_spectrum_by_time(
			self,
			retention_time: float,
			scan_type: MSScanType = MSScanType.All,
			ionization_polarity: Optional[int] = 1,
			ionization_mode: IonizationMode = IonizationMode.Unspecified,
			) -> SpecData:
		"""
		Returns a :class:`pyms_agilent.mhdac.spectrum.SpecData` object for the spectrum at the given retention time.

		If no spectrum is found for the given parameters an empty
		:class:`pyms_agilent.mhdac.spectrum.SpecData` object will be returned.

		:param retention_time:
		:param scan_type:
		:param ionization_polarity: The ionization polarity. 1 = positive, -1 = negative, 0 = +-
		:param ionization_mode:
		"""

		return self._data_reader.get_spectrum_by_time(
				retention_time=retention_time,
				scan_type=scan_type,
				ionization_polarity=ionization_polarity,
				ionization_mode=ionization_mode,
				)

	def get_signal_listing(
			self,
			device_name: str,
			device_type: DeviceType,
			data_type: StoredDataType,
			ordinal: int = 1,
			) -> List[SignalInfo]:
		"""
		Returns a list of signals of the given type available for the given device.

		:param device_name: The name of the device that recorded the signal.
		:param device_type: The type of device that recorded the signal.
		:param data_type:
		:param ordinal:

		Most devices only have :py:enum:mem:`~pyms_agilent.enums.StoredDataType.InstrumentCurves` data,
		although devices such as :py:enum:mem:`~pyms_agilent.enums.DeviceType.VariableWavelengthDetector`
		also have :py:enum:mem:`~pyms_agilent.enums.StoredDataType.Chromatograms` available.

		Usually no data is available for Mass Spectrometry devices; that data is available from
		:meth:`MassSpecDataReader.get_ms_actuals`.
		"""

		return self._data_reader.get_signal_listing(
				device_name=device_name,
				device_type=device_type,
				data_type=data_type,
				ordinal=ordinal,
				)

	def get_ms_actuals(self) -> "MSActuals":
		"""
		Returns the MS Actuals parameters.
		"""

		return self._data_reader.get_ms_actuals()

	def get_sample_data(self, category: SampleCategory = SampleCategory.All) -> Dict[str, Any]:
		"""
		Returns a dictionary of additional metadata about the sample.

		:param category: The category of metadata to return.
		"""

		return self._data_reader.get_sample_data(category)

	def get_timesegment_ids(self) -> List[int]:
		"""
		Returns a list of timesegment IDs.
		"""

		return self._data_reader.get_timesegment_ids()

	@property
	def has_actuals(self) -> bool:
		"""
		Returns whether the datafile contains MS Actuals data.
		"""

		return self._data_reader.has_actuals

	def get_scan_record(self, scan_no: int) -> MSScanRecord:
		"""
		Returns metadata about the scan with the given number.

		:param scan_no:
		"""

		return self._data_reader.get_scan_record(scan_no)
