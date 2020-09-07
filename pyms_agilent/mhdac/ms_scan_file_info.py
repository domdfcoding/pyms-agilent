from typing import List, Optional

from pyms_agilent.mhdac.agilent import DataAnalysis
from pyms_agilent.enums import DeviceType, IonizationMode, MSScanType, MSStorageMode
from pyms_agilent.utils import polarity_map


class MSScanFileInformation:
	"""
	Class to access information about mass spectral data in ``.d`` data files.

	:param BDAMSScanFileInformation: Python.NET object.
	"""

	def __init__(self, BDAMSScanFileInformation: DataAnalysis.BDAMSScanFileInformation):

		self.data_reader = BDAMSScanFileInformation
		self.interface = DataAnalysis.IBDAMSScanFileInformation(self.data_reader)

	@property
	def collision_energies(self) -> List[float]:
		"""
		Returns the collision energies used to acquire the data.
		"""

		return list(self.interface.CollisionEnergies)

	@property
	def compensation_field_values(self) -> List[float]:
		"""
		Returns the compensation field values.
		"""

		return list(self.interface.CompensationFieldValues)

	@property
	def dispersion_field_values(self) -> List[float]:
		"""
		Returns the dispersion field values.
		"""

		return list(self.interface.DispersionFieldValues)

	@property
	def has_ms_data(self) -> bool:
		"""
		Returns whether the file contains mass spectral data.
		"""

		return self.interface.FileHasMassSpectralData

	@property
	def device_type(self) -> DeviceType:
		"""
		Returns the type of device used to acquire the data.
		"""

		return DeviceType(self.interface.DeviceType)

	@property
	def fragmentor_voltages(self) -> List[float]:
		"""
		Returns the fragmentor voltages used to acquire the data.
		"""

		return list(self.interface.FragmentorVoltages)

	# TODO: returning (0.0, 0.0)
	# @property
	# def scan_range(self) -> Tuple[float, float]:
	# 	"""
	# 	Returns the scan range used to acquire the data.
	# 	"""
	#
	# 	return (
	# 			self.interface.MzScanRangeMinimum,
	# 			self.interface.MzScanRangeMaximum,
	# 			)

	# Seems to be the same output as collision energies; same for fragmentor voltages
	# @property
	# def collision_energy(self) -> float:
	# 	"""
	# 	Returns the collision energy used to acquire the data.
	# 	"""
	#
	# 	return list(self.interface.CollisionEnergy)

	@property
	def ionisation_mode(self) -> int:
		"""
		Returns the ionization mode used to acquire the data

		This is the logical bitwise OR of the Ionization Mode values for all scans in the file
		"""

		return IonizationMode(self.interface.IonModes)

	@property
	def ionisation_polarity(self) -> Optional[str]:
		"""
		Returns the ionization polarity used to acquire the data.
		"""

		return polarity_map[self.interface.IonPolarity]

	@property
	def ms_level(self) -> int:
		"""
		Returns the MS level used to acquire the data.
		"""

		return int(self.interface.MSLevel)

	@property
	def scan_types(self) -> int:
		"""
		Returns the MS Scan Type
		This is the logical bitwise OR of the MSScanType values for all scans in the file.
		"""

		return MSScanType(self.interface.ScanTypes)

	@property
	def spectra_format(self) -> MSStorageMode:
		"""
		Returns the format of the spectrum
		"""

		return MSStorageMode(self.interface.SpectraFormat)

	@spectra_format.setter
	def spectra_format(self, mode: MSStorageMode):
		"""
		Sets the format of the spectrum
		"""

		self.interface.SpectraFormat = int(mode)

	@property
	def total_scans(self) -> int:
		"""
		Returns the total number of scans present.
		"""

		return int(self.interface.TotalScansPresent)

	@property
	def has_fixed_cycle_length_data(self) -> bool:
		"""
		Returns whether the data file contains any time segments that have a fixed cycle length.
		"""

		return self.interface.IsFixedCycleLengthDataPresent()

	@property
	def are_multiple_spectra_present_per_scan(self) -> bool:
		"""
		Returns whether the data file contains more than 1 spectra format for each scan.

		This is useful in case of dual mode format stored for each scan.
		"""

		return self.interface.IsMultipleSpectraPerScanPresent()

	@property
	def sim_ions(self) -> List[float]:
		"""
		Returns a list of SIM ions.
		"""

		return list(self.interface.SIMIons)


#  Equals
#  Finalize
#  GetEnumerator
#  GetHashCode
#  GetType
#  MSScanFileInformationIterator
#  MemberwiseClone
#  Overloads
#  ReferenceEquals

# Interface
# ----------
#  Clone
#  Contains
#  GetEnumerator
#  GetMSScanTypeInformation
#  MRMTransitions
#  ScanMethodNumbers
#  ScanTypesInformationCount
#  MassRange  returns 0
#  MzScanRangeMinimum  returns 0
#  MzScanRangeMaximum  returns 0
#  CollisionEnergy  # broken
