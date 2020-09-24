# stdlib
import datetime

# 3rd party
import pytest
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from pyms_agilent.enums import (
		ChromType,
		DataUnit,
		DataValueType,
		DeviceType,
		IonizationMode,
		IRMStatus,
		MeasurementTypeEnum,
		MSScanType,
		MSStorageMode
		)
from pyms_agilent.mhdac.chromatograms import TIC
from pyms_agilent.utils import Range


@pytest.fixture(scope="session")
def tic(reader) -> TIC:
	return reader.get_tic()


class TestTIC:

	def test_abundance_limit(self, tic):
		assert tic.abundance_limit == 16742400.0

	def test_acquired_time_ranges(self, tic):
		assert tic.acquired_time_ranges == [Range(start=0.047216666666666664, stop=14.99765)]

	def test_collision_energy(self, tic):
		assert tic.collision_energy == 0.0

	def test_fragmentor_voltage(self, tic):
		assert tic.fragmentor_voltage == 380.0

	def test_ionization_polarity(self, tic):
		assert tic.ionization_polarity == "+"

	def test_ionization_mode(self, tic):
		assert tic.ionization_mode is IonizationMode.ESI

	def test_ms_level(self, tic):
		assert tic.ms_level == 1

	def test_ms_scan_type(self, tic):
		assert tic.ms_scan_type == MSScanType.Scan

	def test_ms_storage_mode(self, tic):
		assert tic.ms_storage_mode == MSStorageMode.PeakDetectedSpectrum

	def test_mz_of_interest(self, tic):
		assert tic.mz_of_interest == []

	def test_measured_mass_range(self, tic):
		assert tic.measured_mass_range == []

	def test_mz_regions_were_excluded(self, tic):
		assert not tic.mz_regions_were_excluded

	def test_sampling_period(self, tic):
		assert tic.sampling_period == 0.5

	def test_threshold(self, tic):
		assert tic.threshold == 0

	def test_get_x_axis_info(self, tic):
		assert tic.get_x_axis_info() == (DataValueType.AcqTime, DataUnit.Minutes)

	def test_get_y_axis_info(self, tic):
		assert tic.get_y_axis_info() == (DataValueType.IonAbundance, DataUnit.Counts)

	def test_chromatogram_type(self, tic):
		assert tic.chromatogram_type is ChromType.TotalIon

	def test_device_name(self, tic):
		assert tic.device_name == "QTOF"

	def test_device_type(self, tic):
		assert tic.device_type == DeviceType.QuadrupoleTimeOfFlight

	def test_is_chromatogram(self, tic):
		assert tic.is_chromatogram

	def test_is_icp_data(self, tic):
		assert not tic.is_icp_data

	def test_is_cycle_summed(self, tic):
		assert not tic.is_cycle_summed

	def test_is_mass_spectrum(self, tic):
		assert not tic.is_mass_spectrum

	def test_is_primary_mrm(self, tic):
		assert not tic.is_primary_mrm

	def test_is_uv_spectrum(self, tic):
		assert not tic.is_uv_spectrum

	def test_ordinal_number(self, tic):
		assert tic.ordinal_number == 1

	def test_signal_description(self, tic):
		assert tic.signal_description == ''

	def test_signal_name(self, tic):
		assert tic.signal_name == ''

	def test_total_data_points(self, tic, ms_scan_file_info):
		assert tic.total_data_points == 1333
		assert ms_scan_file_info.total_scans == tic.total_data_points

	def test_x_data(self, tic, data_regression: DataRegressionFixture):
		assert tic.x_data[:10] == [
				0.047216666666666664,
				0.05843333333333333,
				0.06966666666666667,
				0.08088333333333333,
				0.09211666666666667,
				0.10333333333333333,
				0.11456666666666666,
				0.12578333333333333,
				0.137,
				0.14823333333333333,
				]
		data_regression.check({"x_data": tic.x_data})

	def test_y_data(self, tic, data_regression: DataRegressionFixture):
		assert tic.y_data[:10] == [
				134909300.0,
				135957800.0,
				131716500.0,
				130281100.0,
				129322300.0,
				127338400.0,
				126183900.0,
				123384600.0,
				121993400.0,
				118873000.0,
				]
		data_regression.check({"y_data": tic.y_data})
