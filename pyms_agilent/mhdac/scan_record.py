from pyms_agilent.enums import IonizationMode, IonPolarity, MSLevel, MSScanType
from pyms_agilent.mhdac.agilent import DataAnalysis

__all__ = ["MSScanRecord"]


class MSScanRecord:
	"""

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
		"""

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

		"""

		return float(self.interface.CompensationField)

	@property
	def dispersionField(self) -> float:
		"""

		"""

		return float(self.interface.DispersionField)

	@property
	def fragmentorVoltage(self) -> float:
		"""
		Returns the Fragmentor Voltage used to acquire the data.
		"""

		return float(self.interface.FragmentorVoltage)

	@property
	def ion_polarity(self) -> IonPolarity:
		"""
		Returns the polarity of the ion, either 1 (positive), 0 (neutral) or -1 (negative).
		"""

		return IonPolarity(self.interface.IonPolarity)

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
		Returns the MZ of interest for the scan, if any.
		"""

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

		:return:
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
		`DesiredMSStorageType == 'Profile'`
		"""  # noqa D400

		return float(self.interface.Tic)

	@property
	def time_segment(self) -> int:
		"""

		"""

		return int(self.interface.TimeSegment)
