#  !/usr/bin/env python
#
#  mass_spec_data_reader.py
"""
The primary interface for reading data files.
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
import os
from typing import Any, Dict, Iterator, List, Mapping, NamedTuple, Tuple, Union

# 3rd party
from domdf_python_tools.typing import PathLike

# this package
from pyms_agilent.enums import DeviceType, IonizationMode, IonPolarity, MSScanType, SampleCategory, StoredDataType
from pyms_agilent.mhdac.agilent import DataAnalysis, FileNotFoundException, NullReferenceException
from pyms_agilent.mhdac.chromatograms import TIC
from pyms_agilent.mhdac.file_information import FileInformation
from pyms_agilent.mhdac.scan_record import MSScanRecord
from pyms_agilent.mhdac.signalinfo import SignalInfo
from pyms_agilent.mhdac.spectrum import SpecData
from pyms_agilent.utils import datatable2dataframe

__all__ = ["MassSpecDataReader", "MSActual", "MSActuals"]


class MassSpecDataReader:
	"""
	The primary interface for reading data files.

	:param filename: The ``.d`` data file to open.

	:raises FileNotFoundError: if the datafile cannot be found.
	:raises IOError: if the datafile cannot be opened for any other reason.
	"""

	def __init__(self, filename: PathLike):
		if not os.path.exists(filename):
			raise FileNotFoundError(filename)

		self.filename: str = str(filename)
		self.data_reader = DataAnalysis.MassSpecDataReader()
		self.interface = DataAnalysis.IMsdrDataReader

		try:
			if not self.interface.OpenDataFile(self.data_reader, self.filename):
				raise OSError(f"Could not open data file '{self.filename}'")  # pragma: no cover
		except FileNotFoundException as e:
			raise FileNotFoundError(str(e).split('\n')[0]) from None

	def close_datafile(self) -> bool:
		"""
		Closes the datafile.

		:return:
		"""

		self.interface.CloseDataFile(self.data_reader)
		return True

	def refresh_datafile(self) -> bool:
		"""
		Refreshes the data file and returns whether new data is present.

		:return: Whether new data is present in the data file
		"""

		# TODO: update stubs
		return self.interface.RefreshDataFile(self.data_reader, True)[1]  # type: ignore

	@property
	def file_information(self) -> FileInformation:
		"""
		Returns a class containing information about the file.
		"""

		return FileInformation(self.interface(self.data_reader).FileInformation)

	def get_tic(self) -> TIC:
		"""
		Returns the total ion chromatogram of the data.
		"""

		return TIC(self.interface(self.data_reader).GetTIC())

	def get_spectrum_by_scan(self, scan_no: int) -> SpecData:
		"""
		Returns a :class:`pyms_agilent.mhdac.spectrum.SpecData` object for the given scan.

		:param scan_no: The scan number.

		:raises: :exc:`ValueError` if the scan number is out of range.
		"""

		# TODO: by number and scan type

		peak_filter = DataAnalysis.MsdrPeakFilter()

		if int(scan_no) < 0:
			raise ValueError("scan_no must be greater than or equal to 0")

		try:
			# Signature is scan_no, peakMSFilter, peakMSMSFilter
			return SpecData(self.interface(self.data_reader).GetSpectrum(int(scan_no), peak_filter, peak_filter))
		except NullReferenceException:
			raise ValueError("scan_no out of range")

	def get_spectrum_by_time(
			self,
			retention_time: float,
			scan_type: MSScanType = MSScanType.All,
			ionization_polarity: int = 1,
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

		:raises: :exc:`ValueError` if the retention time is less than zero or no such scan exists for the given parameters.

		If the requested retention time is beyond the end of the acquired time range the spectrum for
		the latest time will be returned.
		"""

		# TODO: centroid vs scan

		peak_filter = DataAnalysis.MsdrPeakFilter()

		if ionization_polarity is None:
			raise ValueError("'ionization_polarity' cannot be None.")
		elif ionization_polarity > 0:
			ionization_polarity = IonPolarity.Positive  # 0  # I really don't know why it is this way
		elif ionization_polarity < 0:
			ionization_polarity = IonPolarity.Negative  # 1
		elif ionization_polarity == 0:
			ionization_polarity = IonPolarity.Mixed  # 3
		else:
			raise ValueError(
					"Invalid value for 'ionization_polarity'. "
					"Expected a value from the IonPolarity enum."
					)

		if float(retention_time) < 0:
			raise ValueError("retention_time cannot be < 0")

		# try:
		data = SpecData(
				self.interface(self.data_reader).GetSpectrum(
						float(retention_time),
						scan_type,
						ionization_polarity,
						ionization_mode,
						peak_filter,
						)
				)

		try:
			data.scan_id
			return data
		except NullReferenceException:
			raise ValueError("No such scan.")
		# except ArgumentOutOfRangeException:
		# 	raise IndexError

	# def iter_spectra(self):

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

		device = DataAnalysis.IDeviceInfo(DataAnalysis.DeviceInfo())
		device.DeviceName = str(device_name)
		device.DeviceType = int(device_type)  # type: ignore
		device.OrdinalNumber = int(ordinal)

		signal_info_list = [
				SignalInfo(s, self.data_reader) for s in self.data_reader.GetSignalInfo(
						device,
						int(data_type),  # type: ignore
						)
				]
		return signal_info_list

	def get_ms_actuals(self) -> "MSActuals":
		"""
		Returns the MS Actuals parameters.
		"""

		# TODO: Check the type of ActualsInformation.
		# Type hints suggest DataAnalysis.IBDAActuals
		return MSActuals(self.interface(self.data_reader).ActualsInformation)

	def get_sample_data(self, category: SampleCategory = SampleCategory.All) -> Dict[str, Any]:
		"""
		Returns a dictionary of additional metadata about the sample.

		:param category: The category of metadata to return.
		"""

		sample_data = self.interface(self.data_reader).ActualsInformation.GetSampleData(self.filename, category)
		tables = list(sample_data.Tables)

		if tables:
			df = datatable2dataframe(tables[0])
			df = df[["DisplayName", "DisplayValue"]].set_index("DisplayName", drop=True)
			return df.to_dict()["DisplayValue"]

		else:
			return {}

	def get_timesegment_ids(self) -> List[int]:
		"""
		Returns a list of timesegment IDs.
		"""

		return list(self.interface(self.data_reader).ActualsInformation.GetTimeSegmentsIDArray())

	@property
	def has_actuals(self) -> bool:
		"""
		Returns whether the datafile contains MS Actuals data.
		"""

		return DataAnalysis.IBDAActuals(self.interface(self.data_reader).ActualsInformation).IsActualsPresent()

	def get_scan_record(self, scan_no: int) -> MSScanRecord:
		"""
		Returns metadata about the scan with the given number.

		:param scan_no:
		"""

		return MSScanRecord(self.interface.GetScanRecord(self.data_reader, int(scan_no)))


# ActualsInformation
# GetActualsForTimeRange  # TODO
# GetActualsdDefinitionForTimeRange # TODO
# GetActualCollection  # TODO

# data reader
# ----------
# GetEWC
# GetHashCode
# GetNonmsDevices  # Can get from XML
# GetTWC
# GetUVSpectrum  # TODO

# interface
# ----------
# Deisotope
# GetBPC
# GetChromatogram
# GetMSScanInformation  # How does this differ from the one in file_information?
# GetSampleCollection
# MSScanFileInformation  # How does this differ from the one in file_information?
# SchemaDefaultDirectory  # directory of DLL files
# Version  # Version number of something? 8.0

# Getting EIC:
# GetChromatogram(chromFilter: Agilent.MassSpectrometry.DataAnalysis.IBDAChromFilter)
# also Agilent.MassSpectrometry.DataAnalysis.BDAChromFilter

# dr.interface(dr.data_reader).GetSpectrum
# list(DataAnalysis.IBDASpecData(dr.interface(dr.data_reader).GetSpectrum(4.6, 1, 1, 64)).XArray)
"""
Agilent.MassSpectrometry.DataAnalysis.IBDASpecData[] GetSpectrum(Agilent.MassSpectrometry.DataAnalysis.IBDASpecFilter)
Agilent.MassSpectrometry.DataAnalysis.IBDASpecData[] GetSpectrum(Agilent.MassSpectrometry.DataAnalysis.IBDASpecFilter, Agilent.MassSpectrometry.DataAnalysis.IMsdrPeakFilter)
Agilent.MassSpectrometry.DataAnalysis.IBDASpecData GetSpectrum(Agilent.MassSpectrometry.DataAnalysis.IRange[], Agilent.MassSpectrometry.DataAnalysis.IMsdrPeakFilter)
Agilent.MassSpectrometry.DataAnalysis.IBDASpecData GetSpectrum(Agilent.MassSpectrometry.DataAnalysis.IRange, Agilent.MassSpectrometry.DataAnalysis.IMsdrPeakFilter)
Agilent.MassSpectrometry.DataAnalysis.IBDASpecData GetSpectrum(Int32, Agilent.MassSpectrometry.DataAnalysis.IMsdrPeakFilter, Agilent.MassSpectrometry.DataAnalysis.IMsdrPeakFilter)
Agilent.MassSpectrometry.DataAnalysis.IBDASpecData GetSpectrum(Int32, Agilent.MassSpectrometry.DataAnalysis.IMsdrPeakFilter, Agilent.MassSpectrometry.DataAnalysis.IMsdrPeakFilter, Agilent.MassSpectrometry.DataAnalysis.DesiredMSStorageType)
Agilent.MassSpectrometry.DataAnalysis.IBDASpecData GetSpectrum(Double, Agilent.MassSpectrometry.DataAnalysis.MSScanType, Agilent.MassSpectrometry.DataAnalysis.IonPolarity, Agilent.MassSpectrometry.DataAnalysis.IonizationMode, Agilent.MassSpectrometry.DataAnalysis.IMsdrPeakFilter)
Agilent.MassSpectrometry.DataAnalysis.IBDASpecData GetSpectrum(Double, Agilent.MassSpectrometry.DataAnalysis.MSScanType, Agilent.MassSpectrometry.DataAnalysis.IonPolarity, Agilent.MassSpectrometry.DataAnalysis.IonizationMode, Agilent.MassSpectrometry.DataAnalysis.IMsdrPeakFilter, Boolean)
"""
"""
GetSpectrum(IBDASpecFilter* specFilter, IMsdrPeakFilter* peakFilter) -> SAFEARRAY(IBDASpecData*)*


GetSpectrum_2(
	[in] IRange* rtRange,
	[in, optional] IMsdrPeakFilter* peakFilter,
	[out, retval] IBDASpecData** pRetVal
);

GetSpectrum_3(
	[in] SAFEARRAY(IRange*) rtRanges,
	[in, optional] IMsdrPeakFilter* peakFilter,
	[out, retval] IBDASpecData** pRetVal
);



Get scan number
GetSpectrum_6(
	[in] long rowNumber,
	[in, optional] IMsdrPeakFilter* peakMSFilter,
	[in, optional] IMsdrPeakFilter* peakMSMSFilter,
	[out, retval] IBDASpecData** pRetVal
);

GetSpectrum_7(
	[in] double retentionTime,
	[in] MSScanType scanType,
	[in] IonPolarity ionPolarity,
	[in] IonizationMode ionMode,
	[in] IMsdrPeakFilter* peakFilter,
	[in] VARIANT_BOOL peakFilterOnCentroid,
	[out, retval] IBDASpecData** pRetVal
)
"""


class MSActual(NamedTuple):
	"""
	2-element :class:`collections.namedtuple` representing the X- and Y-axis data
	for a parameter recorded by the mass spectrometer.

	:param x_array: The times at which values changed
	:param y_array: The values at those times.

	If the value never changes the ``y_array`` stores the value for the entire run.
	"""  # noqa D400

	x_array: List[float]
	y_array: List[float]


class MSActuals(Mapping[str, MSActual]):
	"""
	Mapping parameter names to values recorded during the analysis.

	The values are :namedtuple:`MSActual` tuples.

	:param BDADataAccess: Python.NET object.
	"""

	_keys: List[str]

	def __init__(self, BDADataAccess: Union[DataAnalysis.BDADataAccess, DataAnalysis.IBDAActuals]):
		self.data_reader = BDADataAccess
		self.interface = DataAnalysis.IBDAActuals(self.data_reader)

	def __getitem__(self, item: str) -> MSActual:
		"""
		Returns the data for the parameter with the given name.

		:param item: The name of the parameter.
		"""

		_, x_array, y_array = self.interface.GetActualValue(item, [0.0], [0.0])
		return MSActual(list(x_array), list(y_array))

	def __len__(self) -> int:
		"""
		Returns the number of parameters recorded.
		"""

		return len(self.keys())

	def __iter__(self) -> Iterator[Tuple[str, MSActual]]:  # type: ignore
		"""
		Iterates over the parameter names and values.
		"""

		for name in self.keys():
			yield name, self[name]

	def keys(self) -> List[str]:  # type: ignore
		"""
		Returns a list of parameter names.
		"""

		if not hasattr(self, "_keys"):
			self._keys = list(self.interface.GetActualNames())

		return self._keys

	def values(self) -> List[MSActual]:  # type: ignore
		"""
		Returns a list of parameter values.
		"""

		return list(x[1] for x in iter(self))  # type: ignore

	def items(self) -> List[Tuple[str, MSActual]]:  # type: ignore
		"""
		Returns a list of parameter values.

		The order corresponds to :meth:`~.keys`.
		"""

		return list(iter(self))  # type: ignore
