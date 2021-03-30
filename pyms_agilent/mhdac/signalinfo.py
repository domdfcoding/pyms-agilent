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
from typing import Any, Dict, MutableMapping, Union

# 3rd party
import attr
from attr_utils.docstrings import add_attrs_doc
from attr_utils.serialise import serde

# this package
from pyms_agilent.enums import DeviceType
from pyms_agilent.mhdac.agilent import DataAnalysis
from pyms_agilent.mhdac.chromatograms import FrozenInstrumentCurve, InstrumentCurve
from pyms_agilent.utils import frozen_comparison

__all__ = ["SignalInfo", "FrozenSignalInfo"]


class SignalInfo:  # pragma: no cover (!Windows)
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

	# TODO: VWD signal

	def get_instrument_curve(self) -> InstrumentCurve:
		"""
		Returns the instrument curve for the signal.
		"""

		return InstrumentCurve(self.msdr.GetSignal(self.data_reader))

	def __repr__(self) -> str:
		"""
		Returns a string representation of the :class:`~pyms_agilent.mhdac.signalinfo.SignalInfo`.
		"""

		return f"{self.__class__.__name__}({self.signal_name}, device={self.device_name}{self.device_ordinal_number})"

	def to_dict(self) -> MutableMapping[str, Any]:
		"""
		Returns a dictionary containing the data of this
		:class:`~pyms_agilent.mhdac.signalinfo.SignalInfo` object.
		"""  # noqa: D400

		return dict(
				device_name=self.device_name,
				device_type=self.device_type,
				device_ordinal_number=self.device_ordinal_number,
				signal_name=self.signal_name,
				instrument_curve=self.get_instrument_curve().freeze(),
				)

	def freeze(self) -> "FrozenSignalInfo":
		"""
		Returns a :class:`~pyms_agilent.mhdac.signalinfo.FrozenSignalInfo` object
		containing the same data as this object.
		"""  # noqa: D400

		return FrozenSignalInfo(**self.to_dict())


def convert_instrument_curve(
		curve: Union[InstrumentCurve, FrozenInstrumentCurve, Dict[str, Any]],
		) -> FrozenInstrumentCurve:  # pragma: no cover (!Windows)
	"""
	Converter for the ``instrument_curve`` parameter in :class:`~.FrozenSignalInfo`.

	:param curve:
	"""

	if isinstance(curve, InstrumentCurve):
		return curve.freeze()  # pragma: no cover
	elif isinstance(curve, FrozenInstrumentCurve):
		return curve
	else:
		return FrozenInstrumentCurve.from_dict(curve)


@serde
@add_attrs_doc
@frozen_comparison(SignalInfo)
@attr.s(slots=True, frozen=True, eq=False, repr=False)
class FrozenSignalInfo:
	"""
	Frozen version of :class:`~pyms_agilent.mhdac.signalinfo.SignalInfo`.
	"""

	#: The name of the device that recorded this signal.
	device_name: str = attr.ib(converter=str)

	#: The type of the device that recorded this signal.
	device_type: DeviceType = attr.ib(converter=DeviceType)

	#: The ordinal number of the device that recorded this signal.
	device_ordinal_number: int = attr.ib(converter=int)

	#: The name of the signal.
	signal_name: str = attr.ib(converter=str)

	instrument_curve: FrozenInstrumentCurve = attr.ib(converter=convert_instrument_curve)

	# TODO: VWD signal

	def get_instrument_curve(self) -> FrozenInstrumentCurve:
		"""
		Returns the instrument curve for the signal.
		"""

		return self.instrument_curve

	def __repr__(self) -> str:
		"""
		Returns a string representation of the :class:`~pyms_agilent.mhdac.signalinfo.FrozenSignalInfo`.
		"""

		return f"{self.__class__.__name__}({self.signal_name}, device={self.device_name}{self.device_ordinal_number})"


# has to be done after FrozenSignalInfo was defined.
frozen_comparison(FrozenSignalInfo)(SignalInfo)
