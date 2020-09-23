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
from typing import Optional

# this package
from pyms_agilent.enums import IonizationMode, MSLevel, MSScanType
from pyms_agilent.mhdac.agilent import DataAnalysis

__all__ = ["MSScanRecord"]

# this package
from pyms_agilent.utils import polarity_map


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
	def collisionEnergy(self) -> float:
		"""
		Returns the Collision Energy used to acquire the scan.
		"""

		return float(self.interface.CollisionEnergy)

	@property
	def compensationField(self) -> float:
		"""
		Returns the value of the compensation field.
		"""

		return float(self.interface.CompensationField)

	@property
	def dispersionField(self) -> float:
		"""
		Returns the value of the dispersion field.
		"""

		return float(self.interface.DispersionField)

	@property
	def fragmentorVoltage(self) -> float:
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
		"""  # noqa RST305

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
