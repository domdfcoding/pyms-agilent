# stdlib
import datetime

# this package
from pyms_agilent.enums import (
		DeviceType,
		IonizationMode,
		IRMStatus,
		MeasurementTypeEnum,
		MSScanType,
		MSStorageMode,
		SeparationTechniqueEnum,
		StoredDataType
		)
from pyms_agilent.mhdac.ms_scan_file_info import FrozenMSScanFileInformation


class TestFileInformation:

	def test_acquisition_time(self, file_info):
		assert file_info.acquisition_time == datetime.datetime(
				year=2020,
				month=3,
				day=3,
				hour=9,
				minute=59,
				second=5,
				tzinfo=datetime.timezone.utc,
				)

	def test_irm_status(self, file_info):
		assert file_info.irm_status == IRMStatus.Success

	def test_datafile_name(self, file_info):
		assert file_info.datafile_name.name == "example1.d"
		assert file_info.datafile_name.suffix == ".d"
		assert file_info.datafile_name.parent.name == "tests"
		assert str(file_info.datafile_name).endswith(r"pyms-agilent\tests\example1.d")

	def test_ms_data_present(self, file_info):
		assert file_info.ms_data_present

	def test_non_ms_data_present(self, file_info):
		assert file_info.non_ms_data_present

	def test_uv_data_present(self, file_info):
		assert not file_info.uv_data_present

	def test_measurement_type(self, file_info):
		assert file_info.measurement_type == MeasurementTypeEnum.Unknown

	def test_separation_technique(self, file_info):
		assert file_info.separation_technique == SeparationTechniqueEnum.LC

	# TODO: ms_scan_file_info

	def test_is_uv_signal_present(self, file_info):
		assert not file_info.is_uv_signal_present(DeviceType.VariableWavelengthDetector, "250nm", "VWD")
		assert not file_info.is_uv_signal_present(DeviceType.VariableWavelengthDetector, "250nm", "Telescope")

	def test_is_datatype_present(self, file_info):
		assert file_info.is_datatype_present(StoredDataType.InstrumentCurves, "TCC")
		assert file_info.is_datatype_present(StoredDataType.InstrumentCurves, "HiP-ALS")
		assert file_info.is_datatype_present(StoredDataType.InstrumentCurves, "VWD")
		assert not file_info.is_datatype_present(StoredDataType.InstrumentCurves, "Telescope")
		assert not file_info.is_datatype_present(StoredDataType.InstrumentCurves, "42")

	def test_get_device_name(self, file_info):
		assert file_info.get_device_name(DeviceType.QuadrupoleTimeOfFlight) == "QTOF"
		assert file_info.get_device_name(DeviceType.ThermostattedColumnCompartment) == "TCC"
		assert file_info.get_device_name(DeviceType.AutoSampler) == "HiP-ALS"
		assert file_info.get_device_name(DeviceType.QuaternaryPump) == "QuatPump"
		assert file_info.get_device_name(DeviceType.VariableWavelengthDetector) == "VWD"
		assert file_info.get_device_name(DeviceType.FluorescenceDetector) is None


class TestMSScanFileInfo:

	def test_collision_energies(self, ms_scan_file_info):
		assert ms_scan_file_info.collision_energies == [0]

	def test_compensation_field_values(self, ms_scan_file_info):
		assert ms_scan_file_info.compensation_field_values == []

	def test_dispersion_field_values(self, ms_scan_file_info):
		assert ms_scan_file_info.dispersion_field_values == []

	def test_fragmentor_voltages(self, ms_scan_file_info):
		assert ms_scan_file_info.fragmentor_voltages == [380.0]

	def test_has_ms_data(self, ms_scan_file_info):
		assert ms_scan_file_info.has_ms_data

	def test_device_type(self, ms_scan_file_info):
		assert ms_scan_file_info.device_type is DeviceType.QuadrupoleTimeOfFlight

	def test_ionisation_mode(self, ms_scan_file_info):
		assert ms_scan_file_info.ionisation_mode is IonizationMode.ESI

	def test_ionisation_polarity(self, ms_scan_file_info):
		assert ms_scan_file_info.ionisation_polarity == "+"

	def test_ms_level(self, ms_scan_file_info):
		assert ms_scan_file_info.ms_level == 1

	def test_scan_types(self, ms_scan_file_info):
		assert ms_scan_file_info.scan_types & MSScanType.Scan

	def test_spectra_format(self, ms_scan_file_info):
		assert ms_scan_file_info.spectra_format is MSStorageMode.Mixed

	def test_total_scans(self, ms_scan_file_info):
		assert ms_scan_file_info.total_scans == 1333

	def test_has_fixed_cycle_length_data(self, ms_scan_file_info):
		assert not ms_scan_file_info.has_fixed_cycle_length_data

	def test_are_multiple_spectra_present_per_scan(self, ms_scan_file_info):
		assert ms_scan_file_info.are_multiple_spectra_present_per_scan

	def test_sim_ions(self, ms_scan_file_info):
		assert ms_scan_file_info.sim_ions == []

	def test_to_dict(self, ms_scan_file_info):
		assert ms_scan_file_info.to_dict() == {
				"collision_energies": [0],
				"compensation_field_values": [],
				"dispersion_field_values": [],
				"has_ms_data": True,
				"device_type": DeviceType.QuadrupoleTimeOfFlight,
				"fragmentor_voltages": [380.0],
				"ionisation_mode": IonizationMode.ESI,
				"ionisation_polarity": "+",
				"ms_level": 1,
				"scan_types": MSScanType.Scan,
				"spectra_format": MSStorageMode.Mixed,
				"total_scans": 1333,
				"has_fixed_cycle_length_data": False,
				"are_multiple_spectra_present_per_scan": True,
				"sim_ions": [],
				}

	def test_freeze(self, ms_scan_file_info):
		assert ms_scan_file_info.freeze() == FrozenMSScanFileInformation(
				collision_energies=[0],
				compensation_field_values=[],
				dispersion_field_values=[],
				has_ms_data=True,
				device_type=DeviceType.QuadrupoleTimeOfFlight,
				fragmentor_voltages=[380.0],
				ionisation_mode=IonizationMode.ESI,
				ionisation_polarity="+",
				ms_level=1,
				scan_types=MSScanType.Scan,
				spectra_format=MSStorageMode.Mixed,
				total_scans=1333,
				has_fixed_cycle_length_data=False,
				are_multiple_spectra_present_per_scan=True,
				sim_ions=[],
				)

	def test_equality(self, ms_scan_file_info):
		expected = FrozenMSScanFileInformation(
				collision_energies=[0],
				compensation_field_values=[],
				dispersion_field_values=[],
				has_ms_data=True,
				device_type=DeviceType.QuadrupoleTimeOfFlight,
				fragmentor_voltages=[380.0],
				ionisation_mode=IonizationMode.ESI,
				ionisation_polarity="+",
				ms_level=1,
				scan_types=MSScanType.Scan,
				spectra_format=MSStorageMode.Mixed,
				total_scans=1333,
				has_fixed_cycle_length_data=False,
				are_multiple_spectra_present_per_scan=True,
				sim_ions=[],
				)

		assert ms_scan_file_info == expected

		assert ms_scan_file_info.to_dict() == expected
		assert ms_scan_file_info == expected.to_dict()

		assert expected == ms_scan_file_info.to_dict()
		assert expected.to_dict() == ms_scan_file_info
