from typing import Any, Dict, Iterator, List, Mapping, NamedTuple, Optional, Tuple

from pyms_agilent.mhdac.agilent import DataAnalysis
from pyms_agilent.mhdac.chromatograms import TIC
from pyms_agilent.enums import DeviceType, IonizationMode, MSScanType, SampleCategory, StoredDataType
from pyms_agilent.mhdac.file_information import FileInformation
from pyms_agilent.mhdac.scan_record import MSScanRecord
from pyms_agilent.mhdac.signal import Signal
from pyms_agilent.mhdac.spectrum import SpecData
from pyms_agilent.utils import datatable2dataframe


class MassSpecDataReader:
	"""

	:param filename: The ``.d`` data file to open.
	"""

	def __init__(self, filename: str):
		self.filename = filename
		self.data_reader = DataAnalysis.MassSpecDataReader()
		self.interface = DataAnalysis.IMsdrDataReader

		if not self.interface.OpenDataFile(self.data_reader, str(filename)):
			raise IOError(f"Could not open data file '{filename}'")

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

		return self.interface.RefreshDataFile(self.data_reader)

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
		Returns a :class:`pyms_agilent.spectrum.SpecData` object for the given scan.

		:param scan_no:
		"""

		# TODO: by number and scan type

		peak_filter = DataAnalysis.MsdrPeakFilter()

		# Signature is scan_no, peakMSFilter, peakMSMSFilter
		return SpecData(self.interface(self.data_reader).GetSpectrum(int(scan_no), peak_filter, peak_filter))

	def get_spectrum_by_time(
			self,
			retention_time: float,
			scan_type: MSScanType = MSScanType.All,
			ionization_polarity: Optional[int] = 1,
			ionization_mode: IonizationMode = IonizationMode.Unspecified,
			) -> SpecData:
		"""
		Returns a :class:`pyms_agilent.spectrum.SpecData` object for the spectrum at the given retention time.

		If no spectrum is found for the given parameters an empty
		:class:`pyms_agilent.mhdac.spectrum.SpecData` object will be returned.

		:param retention_time:
		:param scan_type:
		:param ionization_polarity: The ionization polarity. 1 = positive, -1 = negative, 0 = +-
		:param ionization_mode:
		"""

		# TODO: centroid vs scan

		peak_filter = DataAnalysis.MsdrPeakFilter()

		if ionization_polarity is None:
			ionization_polarity = 2
		elif ionization_polarity > 0:
			ionization_polarity = 0  # I really don't know why it is this way
		elif ionization_polarity < 0:
			ionization_polarity = 1
		elif ionization_polarity == 0:
			ionization_polarity = 3

		return SpecData(self.interface(self.data_reader).GetSpectrum(float(retention_time), scan_type, ionization_polarity, ionization_mode, peak_filter))

	# def iter_spectra(self):

	def get_signal_listing(
			self,
			device_name: str,
			device_type: DeviceType,
			data_type: StoredDataType,
			ordinal: int = 1,
			) -> List[Signal]:
		"""
		Returns a list of signals of the given type available for the given device.

		:param device_name: The name of the device that recorded the signal.
		:param device_type: The type of device that recorded the signal.
		:param data_type:
		:param ordinal:

		:return:

		Most devices only have ``<StoredDataType.InstrumentCurves>`` data,
		although devices such as ``<DeviceType.VariableWavelengthDetector>`` also have
		``<StoredDataType.Chromatograms>`` available.

		Usually no data is available for Mass Spectrometry devices; that data is available from
		:meth:`MassSpecDataReader.get_ms_actuals`.

		"""

		device = DataAnalysis.IDeviceInfo(DataAnalysis.DeviceInfo())
		device.DeviceName = str(device_name)
		device.DeviceType = int(device_type)
		device.OrdinalNumber = int(ordinal)

		signal_info_list = [
				Signal(s, self.data_reader)
				for s in self.data_reader.GetSignalInfo(
						device,
						int(data_type),  # type: ignore
						)]
		return signal_info_list

	def get_ms_actuals(self) -> "MSActuals":
		"""
		Returns the MS Actuals parameters.
		"""

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

		:param scan_no:
		:return:
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
	x_array: List[float]
	y_array: List[float]


class MSActuals(Mapping[str, Tuple[List[float], List[float]]]):
	"""
	Mapping of MS Actuals names to values.

	The values are 2-element tuples of ``(x_array, y_array)``.

	The ``x_array`` stores the times at which values changed;
	the ``y_array`` stores the values at those times;

	If the value never changes the ``y_array`` stores the value for the entire run.

	:param BDADataAccess: Python.NET object.
	"""

	_keys: List[str]

	def __init__(self, BDADataAccess: DataAnalysis.BDADataAccess):
		self.data_reader = BDADataAccess
		self.interface = DataAnalysis.IBDAActuals(self.data_reader)

	def __getitem__(self, item: str) -> MSActual:
		_, x_array, y_array = self.interface.GetActualValue(item, [0.0], [0.0])
		return MSActual(list(x_array), list(y_array))

	def __len__(self) -> int:
		return len(self.keys())

	def __iter__(self) -> Iterator[Tuple[str, MSActual]]:  # type: ignore
		for name in self.keys():
			yield name, self[name]

	def keys(self) -> List[str]:  # type: ignore

		if not hasattr(self, "_keys"):
			self._keys = list(self.interface.GetActualNames())

		return self._keys

	def items(self) -> List[Tuple[str, MSActual]]:  # type: ignore

		return list(iter(self))  # type: ignore
