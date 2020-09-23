#  !/usr/bin/env python
#
#  signalinfo.py
"""
Provides metadata about a signal recorded by the instrument.
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
from typing import Union

# this package
from pyms_agilent.enums import DeviceType
from pyms_agilent.mhdac.agilent import DataAnalysis
from pyms_agilent.mhdac.chromatograms import InstrumentCurve

__all__ = ["SignalInfo"]


class SignalInfo:
	"""
	Provides metadata about a signal recorded by the instrument.

	:param SignalInfo: Python.NET object.
	:param msdr: Python.NET object.
	"""

	def __init__(
			self,
			SignalInfo: Union[DataAnalysis.SignalInfo, DataAnalysis.ISignalInfo],
			msdr: DataAnalysis.MassSpecDataReader
			):
		self.data_reader = SignalInfo
		self.interface = DataAnalysis.ISignalInfo(self.data_reader)
		self.msdr = msdr

	@property
	def device_name(self) -> str:
		"""
		Returns the name of the device that recorded this signal.
		"""

		return str(self.interface.DeviceInformation.DeviceName)

	@property
	def device_type(self) -> DeviceType:
		"""
		Returns the type of the device that recorded this signal.
		"""

		return DeviceType(self.interface.DeviceInformation.DeviceType)

	@property
	def device_ordinal_number(self) -> int:
		"""
		Returns the ordinal number of the device that recorded this signal.
		"""

		return int(self.interface.DeviceInformation.OrdinalNumber)

	@property
	def signal_name(self) -> str:
		"""
		Returns the name of the signal.
		"""

		return str(self.interface.SignalName)

	# TODO: the signal itself

	def get_instrument_curve(self) -> InstrumentCurve:
		"""
		Returns the instrument curve for the signal.
		"""

		return InstrumentCurve(self.msdr.GetSignal(self.data_reader))
