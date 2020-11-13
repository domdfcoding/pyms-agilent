# stdlib
import json
import pathlib
from typing import List

# 3rd party
import pytest
from domdf_python_tools.testing import check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from pyms_agilent.enums import (
		DataUnit,
		DataValueType,
		DeviceType,
		IonizationMode,
		MSLevel,
		MSScanType,
		MSStorageMode,
		SampleCategory,
		SpecType,
		StoredDataType
		)
from pyms_agilent.mhdac.mass_spec_data_reader import MassSpecDataReader, MSActual, MSActuals
from pyms_agilent.mhdac.scan_record import FrozenMSScanRecord, UndefinedMSScanRecord
from pyms_agilent.mhdac.signalinfo import FrozenSignalInfo, SignalInfo
from pyms_agilent.mhdac.spectrum import FrozenSpecData, SpecData
from pyms_agilent.utils import Range, isnan


class TestDataReader:

	def test_reading(self, datafile):
		assert MassSpecDataReader(datafile)

		with pytest.raises(FileNotFoundError, match=r"i_dont_exist.d"):
			MassSpecDataReader("i_dont_exist.d")

		with pytest.raises(
				FileNotFoundError, match=r"File not found: .*\\not_a_datafile.d\\AcqData\\Contents.xml"
				):
			MassSpecDataReader(pathlib.Path(__file__).parent.parent / "not_a_datafile.d")

		assert not MassSpecDataReader(datafile).refresh_datafile()
		assert MassSpecDataReader(datafile).close_datafile()

	def test_has_actuals(self, reader):
		assert reader.has_actuals

	def test_get_timesegment_ids(self, reader):
		assert reader.get_timesegment_ids() == [1]

	def test_get_ms_actuals(self, reader, file_regression: FileRegressionFixture):
		actuals = reader.get_ms_actuals()
		assert isinstance(actuals, MSActuals)
		assert actuals.keys() == [
				"Min Range",
				"TOF Vac",
				"Quad Vac",
				"Rough Vac",
				"PMT",
				"Drying Gas",
				"Gas Temp",
				"Nebulizer",
				"Fragmentor:1",
				"Fragmentor:2",
				"Fragmentor:3",
				"Fragmentor:4",
				"Skimmer(Hex Exit Lens):1",
				"Skimmer(Hex Exit Lens):2",
				"Skimmer(Hex Exit Lens):3",
				"Skimmer(Hex Exit Lens):4",
				"Oct 1 RF Vpp:1",
				"Oct 1 RF Vpp:2",
				"Oct 1 RF Vpp:3",
				"Oct 1 RF Vpp:4",
				"VCap:1",
				"VCap:2",
				"VCap:3",
				"VCap:4",
				"Oct1 DC",
				"Lens 1",
				"Lens 2",
				"Lens 2 RF Enable",
				"Lens 2 RF V",
				"Lens 2 RF Ph",
				"Quad AMU",
				"Quad DC",
				"Post Filter DC",
				"Width Gain",
				"Width Offset",
				"Axis Gain",
				"Axis Offset",
				"Col. Cell Gas",
				"Col. Cell Flow",
				"Hex RF",
				"Hex DC Entr",
				"Hex dV",
				"Cell Entr",
				"Cell Exit",
				"Oct2 DC",
				"Oct 2 RF Vpp",
				"Ion Focus",
				"Slicer",
				"Horiz Q",
				"Vert Q",
				"Top Slit",
				"Bot Slit",
				"Pusher",
				"Puller",
				"Puller Offset",
				"Acc Focus",
				"Mirror Front",
				"Mirror Mid",
				"Mirror Back",
				"MCP",
				"Amp Offset",
				"Turbo1 Speed",
				"Turbo2 Speed",
				"Turbo1 Power",
				"Turbo2 Power",
				"Length of Transients",
				"Vaporizor/Sheath Gas Temp",
				"Calibrant Solution",
				"LC Stream",
				"Charging/Nozzle Voltage",
				"Ion Polarity",
				"Col. Cell Energy",
				"Charge State",
				"Corona",
				"Sheath Gas Flow",
				"Number of Transients",
				"Funnel DC",
				"Funnel Delta HP",
				"Funnel Delta LP",
				"Funnel RF HP",
				"Funnel RF LP",
				"Slicer Position",
				"Collision Energy:1",
				"Collision Energy:2",
				"Collision Energy:3",
				"Collision Energy:4",
				"Drift Tube Temperature",
				"Drift Tube Pressure",
				"Drift Tube Entrance Voltage",
				"Drift Tube Exit Voltage",
				"High Pressure Funnel Exit",
				"High Pressure Funnel Delta",
				"High Pressure Funnel RF",
				"HP Funnel Pressure",
				"IM Hex Entrance",
				"IM Hex RF",
				"Non Turbo Pump Speed",
				"Rear Funnel Entrance",
				"Rear Funnel Exit",
				"Rear Funnel RF",
				"Trap Entrance",
				"Trap Entrance Grid Delta",
				"Trap Entrance Grid Low",
				"Trap Exit",
				"Trap Exit Grid 1 Delta",
				"Trap Exit Grid 1 Low",
				"Trap Exit Grid 2 Delta",
				"Trap Exit Grid 2 Low",
				"Trap Funnel Delta",
				"Trap Funnel Exit",
				"Trap Funnel Pressure",
				"Trap Funnel RF",
				"Turbo Pump Power",
				]

		values = actuals.values()
		assert len(values) == len(actuals.keys()) == len(actuals) == len(list(actuals)) == len(actuals.items())

		assert isinstance(values[0], MSActual)
		assert values[0].x_array == [0.047216666666666664]
		assert values[0].y_array == [8576.0]

		assert actuals["TOF Vac"].x_array[:4] == [
				0.047216666666666664,
				0.14823333333333333,
				0.28291666666666665,
				1.0910332682291666,
				]
		assert actuals["TOF Vac"].y_array[:4] == [
				2.1993034238221298e-07,
				2.1747149503426044e-07,
				2.1993034238221298e-07,
				2.1869746547054092e-07,
				]

		assert actuals.items()[2][0] == "Quad Vac"
		assert isinstance(actuals.items()[2][1], MSActual)

		check_file_regression(json.dumps(dict(actuals)), file_regression, extension=".json")

	times = {
			"03/03/2020 09:59:05 (UTC+00:00)",  # locally
			"3/3/2020 9:59:05 AM (UTC+00:00)",  # github actions
			}

	def test_get_sample_data_all(self, reader, file_regression: FileRegressionFixture):
		sample_data = reader.get_sample_data()

		if sample_data["Acquisition Time"] in self.times:
			del sample_data["Acquisition Time"]

		if sample_data["Acquisition Time (Local)"] in self.times:
			del sample_data["Acquisition Time (Local)"]

		self.check_json_regression(sample_data, file_regression)

	def test_get_sample_data_unspecified(self, reader, file_regression: FileRegressionFixture):
		self.check_json_regression(reader.get_sample_data(SampleCategory.Unspecified), file_regression)

	def test_get_sample_data_general(self, reader, file_regression: FileRegressionFixture):

		sample_data = reader.get_sample_data(SampleCategory.General)

		if sample_data["Acquisition Time"] in self.times:
			del sample_data["Acquisition Time"]

		if sample_data["Acquisition Time (Local)"] in self.times:
			del sample_data["Acquisition Time (Local)"]

		self.check_json_regression(sample_data, file_regression)

	def test_get_sample_data_optimization_params(self, reader, file_regression: FileRegressionFixture):
		self.check_json_regression(reader.get_sample_data(SampleCategory.OptimizationParams), file_regression)

	def test_get_sample_data_compound_params(self, reader, file_regression: FileRegressionFixture):
		self.check_json_regression(reader.get_sample_data(SampleCategory.CompoundParams), file_regression)

	def test_get_sample_data_mass_params(self, reader, file_regression: FileRegressionFixture):
		self.check_json_regression(reader.get_sample_data(SampleCategory.MassParams), file_regression)

	def test_get_sample_data_custom_params(self, reader, file_regression: FileRegressionFixture):
		self.check_json_regression(reader.get_sample_data(SampleCategory.CustomParams), file_regression)

	def test_get_sample_data_user_params(self, reader, file_regression: FileRegressionFixture):
		self.check_json_regression(reader.get_sample_data(SampleCategory.UserParams), file_regression)

	def check_json_regression(self, obj: object, file_regression: FileRegressionFixture, **kwargs):
		kwargs["indent"] = kwargs.get("indent", 2)
		check_file_regression(json.dumps(obj, **kwargs), file_regression, extension=".json")

	def check_signal_regression(self, signals: List[SignalInfo], file_regression: FileRegressionFixture):
		self.check_json_regression(
				[signal.freeze().to_dict(convert_values=True) for signal in signals],
				file_regression,
				)

	def test_get_signal_listing_vwd_curve(self, reader, file_regression: FileRegressionFixture):
		self.check_signal_regression(
				reader.get_signal_listing(
						"VWD",
						DeviceType.VariableWavelengthDetector,
						StoredDataType.InstrumentCurves,
						),
				file_regression,
				)

	def test_get_signal_listing_vwd_chrom(self, reader, file_regression: FileRegressionFixture):
		self.check_signal_regression(
				reader.get_signal_listing(
						"VWD",
						DeviceType.VariableWavelengthDetector,
						StoredDataType.Chromatograms,
						),
				file_regression,
				)

	def test_get_signal_listing_tcc(self, reader, file_regression: FileRegressionFixture):
		self.check_signal_regression(
				reader.get_signal_listing(
						"TCC",
						DeviceType.ThermostattedColumnCompartment,
						StoredDataType.InstrumentCurves,
						),
				file_regression,
				)

	def test_get_signal_listing_autosampler(self, reader, file_regression: FileRegressionFixture):
		self.check_signal_regression(
				reader.get_signal_listing(
						"HiP-ALS",
						DeviceType.AutoSampler,
						StoredDataType.InstrumentCurves,
						),
				file_regression,
				)

	def test_get_signal_listing_pump(self, reader, file_regression: FileRegressionFixture):
		self.check_signal_regression(
				reader.get_signal_listing(
						"QuatPump",
						DeviceType.QuaternaryPump,
						StoredDataType.InstrumentCurves,
						),
				file_regression,
				)

	def test_get_signal_listing_error(self, reader, file_regression: FileRegressionFixture):
		assert reader.get_signal_listing(
				"Telescope",
				DeviceType.QuaternaryPump,
				StoredDataType.InstrumentCurves,
				) == []

	def test_signal_serialisation(self, reader, file_regression: FileRegressionFixture):
		signal = reader.get_signal_listing(
				"HiP-ALS",
				DeviceType.AutoSampler,
				StoredDataType.InstrumentCurves,
				)[0].freeze()

		assert FrozenSignalInfo.from_dict(signal.to_dict(convert_values=True)) == signal
		assert FrozenSignalInfo.from_dict(json.loads(json.dumps(signal.to_dict(convert_values=True)))) == signal

	def test_signal_equality(self, reader):
		signal = reader.get_signal_listing(
				"HiP-ALS",
				DeviceType.AutoSampler,
				StoredDataType.InstrumentCurves,
				)[0]

		assert signal == signal.freeze()
		left = signal.get_instrument_curve().freeze()
		right = signal.freeze().get_instrument_curve()
		assert left == right == signal.freeze().instrument_curve

	def test_signalinfo_repr(self, reader):
		signal = reader.get_signal_listing(
				"VWD",
				DeviceType.AutoSampler,
				StoredDataType.InstrumentCurves,
				)[6]
		assert repr(signal) == "SignalInfo(T, device=VWD1)"
		assert repr(signal.freeze()) == "FrozenSignalInfo(T, device=VWD1)"

	def test_get_scan_record(self, reader):
		expected = FrozenMSScanRecord(
				base_peak_intensity=755713.0,
				base_peak_mz=122.09504758586642,
				collision_energy=0.0,
				compensation_field=float("nan"),
				dispersion_field=float("nan"),
				fragmentor_voltage=380.0,
				ion_polarity='+',
				ionization_mode=IonizationMode.ESI,
				is_collision_energy_dynamic=False,
				is_fragmentor_voltage_dynamic=False,
				ms_level=MSLevel.MS,
				ms_scan_type=MSScanType.Scan,
				mz_of_interest=0.0,
				retention_time=0.047216666666666664,
				scan_id=2841,
				tic=134909337.0,
				time_segment=1,
				)

		assert expected == expected

		assert expected == FrozenMSScanRecord(
				base_peak_intensity=755713.0,
				base_peak_mz=122.09504758586642,
				collision_energy=0.0,
				compensation_field=float("nan"),
				dispersion_field=float("nan"),
				fragmentor_voltage=380.0,
				ion_polarity='+',
				ionization_mode=IonizationMode.ESI,
				is_collision_energy_dynamic=False,
				is_fragmentor_voltage_dynamic=False,
				ms_level=MSLevel.MS,
				ms_scan_type=MSScanType.Scan,
				mz_of_interest=0.0,
				retention_time=0.047216666666666664,
				scan_id=2841,
				tic=134909337.0,
				time_segment=1,
				)

		record = reader.get_scan_record(0)

		assert record == expected
		assert record.freeze() == expected

		record = reader.get_scan_record(-1)

		assert record == UndefinedMSScanRecord
		assert record.freeze() == UndefinedMSScanRecord

		record = reader.get_scan_record(1000000)

		assert record == UndefinedMSScanRecord
		assert record.freeze() == UndefinedMSScanRecord

	def test_get_spectrum_by_scan(self, reader, datadir):
		# TODO: MS2

		spectrum = reader.get_spectrum_by_scan(0)

		assert isinstance(spectrum, SpecData)
		assert isinstance(spectrum.freeze(), FrozenSpecData)

		expected = FrozenSpecData(
				abundance_limit=16742400.0,
				acquired_time_ranges=[Range(0.047216666666666664, 0.047216666666666664)],
				chrom_peak_index=-1,
				collision_energy=0.0,
				compensation_field=float("nan"),
				device_name="QTOF",
				device_type=DeviceType.QuadrupoleTimeOfFlight,
				dispersion_field=float("nan"),
				fragmentor_voltage=380.0,
				x_axis_info=(DataValueType.MassToCharge, DataUnit.Thomsons),
				y_axis_info=(DataValueType.IonAbundance, DataUnit.Counts),
				ionization_polarity='+',
				ionization_mode=IonizationMode.ESI,
				is_chromatogram=False,
				is_data_in_mass_unit=True,
				is_mass_spectrum=True,
				is_icp_data=False,
				is_uv_spectrum=False,
				ms_level=MSLevel.MS,
				ms_scan_type=MSScanType.Scan,
				ms_storage_mode=MSStorageMode.PeakDetectedSpectrum,
				mz_of_interest=[],
				measured_mass_range=Range(40.05473406265757, 999.1105542357848),
				ordinal_number=1,
				parent_scan_id=0,
				sampling_period=0.5,
				scan_id=2841,
				spectrum_type=SpecType.TofMassSpectrum,
				threshold=0.0,
				total_data_points=6000,
				total_scan_count=1,
				x_data=json.loads((datadir / "x_data.json").read_text()),
				y_data=json.loads((datadir / "y_data.json").read_text()),
				)

		assert spectrum.freeze() == expected

		assert isinstance(spectrum.acquired_time_ranges, list)
		assert isinstance(spectrum.acquired_time_ranges[0], Range)

		left = {k: v for k, v in spectrum.to_dict().items() if not isnan(v) and k not in {"x_data", "y_data"}}
		right = {k: v for k, v in expected.to_dict().items() if not isnan(v) and k not in {"x_data", "y_data"}}
		assert left == right

		assert spectrum == expected
		assert spectrum.to_dict() == expected
		assert spectrum.x_data == expected.x_data
		assert expected.to_dict() == spectrum

		assert spectrum.get_x_axis_info() == expected.get_x_axis_info() == expected.x_axis_info
		assert spectrum.get_y_axis_info() == expected.get_y_axis_info() == expected.y_axis_info

		with pytest.raises(ValueError, match="scan_no must be greater than or equal to 0"):
			reader.get_spectrum_by_scan(-1)

		reader.get_spectrum_by_scan(100)
		reader.get_spectrum_by_scan(1000)

		with pytest.raises(ValueError, match="scan_no out of range"):
			reader.get_spectrum_by_scan(10000)

		with pytest.raises(ValueError, match="scan_no out of range"):
			reader.get_spectrum_by_scan(1000000)

	def test_get_spectrum_by_time(self, reader, datadir):
		# TODO: MS2

		spectrum = reader.get_spectrum_by_time(
				0, scan_type=MSScanType.Scan, ionization_polarity=1, ionization_mode=IonizationMode.ESI
				)

		assert isinstance(spectrum, SpecData)

		assert isinstance(spectrum.freeze(), FrozenSpecData)

		assert spectrum.freeze() == FrozenSpecData(
				abundance_limit=16742400.0,
				acquired_time_ranges=[Range(0.047216666666666664, 0.047216666666666664)],
				chrom_peak_index=-1,
				collision_energy=0.0,
				compensation_field=float("nan"),
				device_name="QTOF",
				device_type=DeviceType.QuadrupoleTimeOfFlight,
				dispersion_field=float("nan"),
				fragmentor_voltage=380.0,
				x_axis_info=(DataValueType.MassToCharge, DataUnit.Thomsons),
				y_axis_info=(DataValueType.IonAbundance, DataUnit.Counts),
				ionization_polarity='+',
				ionization_mode=IonizationMode.ESI,
				is_chromatogram=False,
				is_data_in_mass_unit=True,
				is_mass_spectrum=True,
				is_icp_data=False,
				is_uv_spectrum=False,
				ms_level=MSLevel.MS,
				ms_scan_type=MSScanType.Scan,
				ms_storage_mode=MSStorageMode.PeakDetectedSpectrum,
				mz_of_interest=[],
				measured_mass_range=Range(40.05473406265757, 999.1105542357848),
				ordinal_number=1,
				parent_scan_id=0,
				sampling_period=0.5,
				scan_id=2841,
				spectrum_type=SpecType.TofMassSpectrum,
				threshold=0.0,
				total_data_points=6000,
				total_scan_count=1,
				x_data=json.loads((datadir / "x_data.json").read_text()),
				y_data=json.loads((datadir / "y_data.json").read_text()),
				)

		with pytest.raises(ValueError, match="retention_time cannot be < 0"):
			reader.get_spectrum_by_time(-1)

		last_spectrum = FrozenSpecData(
				abundance_limit=16742400.0,
				acquired_time_ranges=[Range(14.99765, 14.99765)],
				chrom_peak_index=-1,
				collision_energy=0.0,
				compensation_field=float("nan"),
				device_name="QTOF",
				device_type=DeviceType.QuadrupoleTimeOfFlight,
				dispersion_field=float("nan"),
				fragmentor_voltage=380.0,
				x_axis_info=(DataValueType.MassToCharge, DataUnit.Thomsons),
				y_axis_info=(DataValueType.IonAbundance, DataUnit.Counts),
				ionization_polarity='+',
				ionization_mode=IonizationMode.ESI,
				is_chromatogram=False,
				is_data_in_mass_unit=True,
				is_mass_spectrum=True,
				is_icp_data=False,
				is_uv_spectrum=False,
				ms_level=MSLevel.MS,
				ms_scan_type=MSScanType.Scan,
				ms_storage_mode=MSStorageMode.PeakDetectedSpectrum,
				mz_of_interest=[],
				measured_mass_range=Range(40.05794500784706, 998.9613817604375),
				ordinal_number=1,
				parent_scan_id=0,
				sampling_period=0.5,
				scan_id=899867,
				spectrum_type=SpecType.TofMassSpectrum,
				threshold=0.0,
				total_data_points=6000,
				total_scan_count=1,
				x_data=json.loads((datadir / "last_scan_x_data.json").read_text()),
				y_data=json.loads((datadir / "last_scan_y_data.json").read_text()),
				)

		assert reader.get_spectrum_by_time(14.99765).freeze().x_data == last_spectrum.x_data
		assert reader.get_spectrum_by_time(14.99765).freeze().y_data == last_spectrum.y_data

		assert reader.get_spectrum_by_time(14.99765).freeze() == last_spectrum
		assert reader.get_spectrum_by_time(1000000).freeze() == last_spectrum
		assert reader.get_spectrum_by_time(100000000000000000000000).freeze() == last_spectrum

		# Different scan type
		with pytest.raises(ValueError, match="No such scan."):
			reader.get_spectrum_by_time(0, scan_type=MSScanType.MultipleReaction)

		# Different polarity
		with pytest.raises(ValueError, match="No such scan."):
			reader.get_spectrum_by_time(0, ionization_polarity=-1)

		# Different ionization mode
		with pytest.raises(ValueError, match="No such scan."):
			reader.get_spectrum_by_time(0, ionization_mode=IonizationMode.Appi)

		# All 3
		with pytest.raises(ValueError, match="No such scan."):
			reader.get_spectrum_by_time(
					0,
					scan_type=MSScanType.MultipleReaction,
					ionization_polarity=-1,
					ionization_mode=IonizationMode.Appi,
					)

		with pytest.raises(ValueError, match="'ionization_polarity' cannot be None."):
			reader.get_spectrum_by_time(0, ionization_polarity=None)

		# With polarity of 0 spectra for either pos and neg will be returned.
		assert reader.get_spectrum_by_time(14.99765, ionization_polarity=0) == last_spectrum
