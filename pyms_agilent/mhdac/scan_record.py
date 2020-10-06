#  !/usr/bin/env python
#
#  scan_record.py
"""
Provides metadata about a single scan.
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
from typing import Any, MutableMapping, Optional

# 3rd party
import attr
from attr_utils.pprinter import pretty_repr
from attr_utils.serialise import serde

# this package
from pyms_agilent.enums import IonizationMode, MSLevel, MSScanType
from pyms_agilent.mhdac.agilent import DataAnalysis
from pyms_agilent.utils import frozen_comparison, isnan, polarity_map

__all__ = ["MSScanRecord", "FrozenMSScanRecord", "UndefinedMSScanRecord"]


class MSScanRecord:
	"""
	Provides metadata about a single scan.

	:param MSScanRecord: A Python.NET object
	"""

	def __init__(self, MSScanRecord: DataAnalysis.MSScanRecord):
		self.data_reader = MSScanRecord
		self.interface = DataAnalysis.IMSScanRecord(self.data_reader)

	@property
	def base_peak_intensity(self) -> float:
		"""
		Returns the intensity of the base peak in the scan.

		The base peak is the most intense peak.
		"""

		return float(self.interface.BasePeakIntensity)

	@property
	def base_peak_mz(self) -> float:
		"""
		Returns the |mz| of the base peak in the scan.

		The base peak is the most intense peak.
		"""  # noqa RST305

		return float(self.interface.BasePeakMZ)

	@property
	def collision_energy(self) -> float:
		"""
		Returns the Collision Energy used to acquire the scan.
		"""

		return float(self.interface.CollisionEnergy)

	@property
	def compensation_field(self) -> float:
		"""
		Returns the value of the compensation field.
		"""

		return float(self.interface.CompensationField)

	@property
	def dispersion_field(self) -> float:
		"""
		Returns the value of the dispersion field.
		"""

		return float(self.interface.DispersionField)

	@property
	def fragmentor_voltage(self) -> float:
		"""
		Returns the Fragmentor Voltage used to acquire the data.
		"""

		return float(self.interface.FragmentorVoltage)

	@property
	def ion_polarity(self) -> Optional[str]:
		"""
		Returns the polarity of the ion.
		"""

		return polarity_map[self.interface.IonPolarity]

	@property
	def ionization_mode(self) -> IonizationMode:
		"""
		Returns the Ionization Mode used to acquire the data.
		"""

		return IonizationMode(self.interface.IonizationMode)

	@property
	def is_collision_energy_dynamic(self) -> bool:
		"""
		Returns whether the Collision Energy is dynamic.
		"""

		return bool(self.interface.IsCollisionEnergyDynamic)

	@property
	def is_fragmentor_voltage_dynamic(self) -> bool:
		"""
		Returns whether the Fragmentor Voltage is dynamic.
		"""

		return bool(self.interface.IsFragmentorVoltageDynamic)

	@property
	def ms_level(self) -> MSLevel:
		"""
		Returns the Mass Spectrometry level e.g. MS or MSMS.
		"""

		return MSLevel(self.interface.MSLevel)

	@property
	def ms_scan_type(self) -> MSScanType:
		"""
		Returns the type of Mass Spectrometry Scan.
		"""

		return MSScanType(self.interface.MSScanType)

	@property
	def mz_of_interest(self) -> float:
		"""
		Returns the |mz| of interest for the scan, if any.
		"""

		# noqa RST305

		mz = float(self.interface.MZOfInterest)

		# if mz == 0.0:
		# 	return None
		# else:
		# 	return mz

		return mz

	@property
	def retention_time(self) -> float:
		"""
		Returns the retention time of the scan, in minutes.
		"""

		return float(self.interface.RetentionTime)

	@property
	def scan_id(self) -> int:
		"""
		Returns the ID of the Scan.
		"""

		return int(self.interface.ScanID)

	@property
	def tic(self) -> float:
		"""
		Returns the summed intensity of all ions in the scan with
		``DesiredMSStorageType == 'Profile'``.
		"""  # noqa D400

		return float(self.interface.Tic)

	@property
	def time_segment(self) -> int:
		"""
		Returns the time segment the scan belongs to.
		"""

		return int(self.interface.TimeSegment)

	def to_dict(self) -> MutableMapping[str, Any]:
		"""
		Returns a dictionary containing the data of this
		:class:`~pyms_agilent.mhdac.scan_record.MSScanRecord` object.
		"""

		return dict(
				base_peak_intensity=self.base_peak_intensity,
				base_peak_mz=self.base_peak_mz,
				collision_energy=self.collision_energy,
				compensation_field=self.compensation_field,
				dispersion_field=self.dispersion_field,
				fragmentor_voltage=self.fragmentor_voltage,
				ion_polarity=self.ion_polarity,
				ionization_mode=self.ionization_mode,
				is_collision_energy_dynamic=self.is_collision_energy_dynamic,
				is_fragmentor_voltage_dynamic=self.is_fragmentor_voltage_dynamic,
				ms_level=self.ms_level,
				ms_scan_type=self.ms_scan_type,
				mz_of_interest=self.mz_of_interest,
				retention_time=self.retention_time,
				scan_id=self.scan_id,
				tic=self.tic,
				time_segment=self.time_segment,
				)

	def freeze(self) -> "FrozenMSScanRecord":
		"""
		Returns a :class:`~pyms_agilent.mhdac.scan_record.FrozenMSScanRecord` object
		containing the same data as this object.
		"""

		return FrozenMSScanRecord(**self.to_dict())

	def is_undefined(self) -> bool:
		"""
		Returns whether the scan record is undefined.

		If the scan record is undefined this is usually a result
		of requesting a scan that doesn't exist.
		"""

		return self == UndefinedMSScanRecord


@serde
@pretty_repr
@frozen_comparison(MSScanRecord)
@attr.s(slots=True, frozen=True, eq=False)
class FrozenMSScanRecord:
	"""
	Frozen version of :class:`~.MSScanRecord`.

	Provides metadata about a single scan.
	"""

	#: The intensity of the base peak in the scan.
	base_peak_intensity: float = attr.ib(converter=float)

	#: Returns the |mz| of the base peak in the scan.
	base_peak_mz: float = attr.ib(converter=float)

	#: Returns the Collision Energy used to acquire the scan.
	collision_energy: float = attr.ib(converter=float)

	#: Returns the value of the compensation field.
	compensation_field: float = attr.ib(converter=float)

	#: Returns the value of the dispersion field.
	dispersion_field: float = attr.ib(converter=float)

	#: Returns the Fragmentor Voltage used to acquire the data.
	fragmentor_voltage: float = attr.ib(converter=float)

	#: Returns the polarity of the ion.
	ion_polarity: Optional[str] = attr.ib()

	#: Returns the Ionization Mode used to acquire the data.
	ionization_mode: IonizationMode = attr.ib(converter=IonizationMode)

	#: Returns whether the Collision Energy is dynamic.
	is_collision_energy_dynamic: bool = attr.ib(converter=bool)

	#: Returns whether the Fragmentor Voltage is dynamic.
	is_fragmentor_voltage_dynamic: bool = attr.ib(converter=bool)

	#: Returns the Mass Spectrometry level e.g. MS or MSMS.
	ms_level: MSLevel = attr.ib(converter=MSLevel)

	#: Returns the type of Mass Spectrometry Scan.
	ms_scan_type: MSScanType = attr.ib(converter=MSScanType)

	#: Returns the |mz| of interest for the scan, if any.
	mz_of_interest: float = attr.ib(converter=float)

	#: Returns the retention time of the scan, in minutes.
	retention_time: float = attr.ib(converter=float)

	#: Returns the ID of the Scan.
	scan_id: int = attr.ib(converter=int)

	#: Returns the summed intensity of all ions in the scan with ``DesiredMSStorageType == 'Profile'``
	tic: float = attr.ib(converter=float)

	#: Returns the time segment the scan belongs to.
	time_segment: int = attr.ib(converter=int)

	def is_undefined(self) -> bool:
		"""
		Returns whether the scan record is undefined.

		If the scan record is undefined this is usually a result
		of requesting a scan that doesn't exist.
		"""

		return self == UndefinedMSScanRecord


# has to be done after FrozenMSScanRecord was defined.
frozen_comparison(FrozenMSScanRecord)(MSScanRecord)

#: Represents an MSScanRecord that is undefined, usually as a result of requesting a scan that doesn't exist.
UndefinedMSScanRecord = FrozenMSScanRecord(
		base_peak_intensity=0.0,
		base_peak_mz=0.0,
		collision_energy=0.0,
		compensation_field=0.0,
		dispersion_field=0.0,
		fragmentor_voltage=0.0,
		ion_polarity="+",
		ionization_mode=IonizationMode.Unspecified,
		is_collision_energy_dynamic=False,
		is_fragmentor_voltage_dynamic=False,
		ms_level=MSLevel.All,
		ms_scan_type=MSScanType.Unspecified,
		mz_of_interest=0.0,
		retention_time=0.0,
		scan_id=0,
		tic=0.0,
		time_segment=0
		)
