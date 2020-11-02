#  !/usr/bin/env python
#
#  ms_scan_file_info.py
"""
Provides access to information about mass spectral data in ``.d`` data files.
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
from typing import Any, Iterable, List, MutableMapping, Optional

# 3rd party
import attr
from attr_utils.pprinter import pretty_repr
from attr_utils.serialise import serde
from domdf_python_tools.utils import strtobool

# this package
from pyms_agilent.enums import DeviceType, IonizationMode, MSScanType, MSStorageMode
from pyms_agilent.mhdac.agilent import DataAnalysis
from pyms_agilent.utils import frozen_comparison, polarity_map

__all__ = ["MSScanFileInformation", "FrozenMSScanFileInformation"]


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
	def ionisation_mode(self) -> IonizationMode:
		"""
		Returns the ionization mode used to acquire the data.

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
	def scan_types(self) -> MSScanType:
		"""
		Returns the MS Scan Type.

		This is the logical bitwise OR of the MSScanType values for all scans in the file.
		"""

		return MSScanType(self.interface.ScanTypes)

	@property
	def spectra_format(self) -> MSStorageMode:
		"""
		Returns the format of the spectrum.
		"""

		return MSStorageMode(self.interface.SpectraFormat)

	#
	# @spectra_format.setter
	# def spectra_format(self, mode: MSStorageMode):
	# 	"""
	# 	Sets the format of the spectrum.
	# 	"""
	#
	# 	self.interface.SpectraFormat = int(mode)

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

	def to_dict(self) -> MutableMapping[str, Any]:
		"""
		Returns a dictionary containing the data of this
		:class:`~pyms_agilent.mhdac.ms_scan_file_info.MSScanFileInformation` object.
		"""  # noqa: D400

		return dict(
				collision_energies=self.collision_energies,
				compensation_field_values=self.compensation_field_values,
				dispersion_field_values=self.dispersion_field_values,
				has_ms_data=self.has_ms_data,
				device_type=self.device_type,
				fragmentor_voltages=self.fragmentor_voltages,
				ionisation_mode=self.ionisation_mode,
				ionisation_polarity=self.ionisation_polarity,
				ms_level=self.ms_level,
				scan_types=self.scan_types,
				spectra_format=self.spectra_format,
				total_scans=self.total_scans,
				has_fixed_cycle_length_data=self.has_fixed_cycle_length_data,
				are_multiple_spectra_present_per_scan=self.are_multiple_spectra_present_per_scan,
				sim_ions=self.sim_ions,
				)

	def freeze(self) -> "FrozenMSScanFileInformation":
		"""
		Returns a :class:`~pyms_agilent.mhdac.ms_scan_file_info.FrozenMSScanFileInformation`
		object containing the same data as this object.
		"""  # noqa: D400

		return FrozenMSScanFileInformation(**self.to_dict())


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


def _float_list_converter(iterable: Iterable[float]):
	return list(iterable)


@serde
@pretty_repr
@frozen_comparison(MSScanFileInformation)
@attr.s(slots=True, frozen=True, eq=False)
class FrozenMSScanFileInformation:
	"""
	Frozen version of :class:`~.MSScanFileInformation`.

	Provides information about mass spectral data in ``.d`` data files.
	"""

	#: The collision energies used to acquire the data.
	collision_energies: List[float] = attr.ib(converter=_float_list_converter)

	#: The compensation field values.
	compensation_field_values: List[float] = attr.ib(converter=_float_list_converter)

	#: The dispersion field values.
	dispersion_field_values: List[float] = attr.ib(converter=_float_list_converter)

	#: Returns whether the file contains mass spectral data.
	has_ms_data: bool = attr.ib(converter=strtobool)

	#: The type of device used to acquire the data.
	device_type: DeviceType = attr.ib(converter=DeviceType)

	#: The fragmentor voltages used to acquire the data.
	fragmentor_voltages: List[float] = attr.ib(converter=_float_list_converter)

	ionisation_mode: IonizationMode = attr.ib(converter=IonizationMode)
	"""
	The ionization mode used to acquire the data.

	This is the logical bitwise OR of the Ionization Mode values for all scans in the file
	"""

	#: The ionization polarity used to acquire the data.
	ionisation_polarity: Optional[str] = attr.ib()

	#: The MS level used to acquire the data.
	ms_level: int = attr.ib(converter=int)

	scan_types: MSScanType = attr.ib(converter=MSScanType)
	"""
	The MS Scan Type.

	This is the logical bitwise OR of the MSScanType values for all scans in the file.
	"""

	#: The format of the spectrum.
	spectra_format: MSStorageMode = attr.ib(converter=MSStorageMode)

	#: The total number of scans present.
	total_scans: int = attr.ib(converter=int)

	#: Returns whether the data file contains any time segments that have a fixed cycle length.
	has_fixed_cycle_length_data: bool = attr.ib(converter=strtobool)

	are_multiple_spectra_present_per_scan: bool = attr.ib(converter=strtobool)
	"""
	Returns whether the data file contains more than 1 spectra format for each scan.

	This is useful in case of dual mode format stored for each scan.
	"""

	#: Returns a list of SIM ions.
	sim_ions: List[float] = attr.ib(converter=_float_list_converter)


# has to be done after FrozenMSScanFileInformation was defined.
frozen_comparison(FrozenMSScanFileInformation)(MSScanFileInformation)
