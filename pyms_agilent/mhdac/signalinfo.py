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
