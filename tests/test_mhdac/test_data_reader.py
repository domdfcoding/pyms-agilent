# stdlib
import json

# 3rd party
from typing import List

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from pyms_agilent.enums import DeviceType, SampleCategory, StoredDataType
from pyms_agilent.mhdac.mass_spec_data_reader import MassSpecDataReader, MSActual, MSActuals
from pyms_agilent.mhdac.signalinfo import FrozenSignalInfo, SignalInfo


class TestDataReader:

	def test_reading(self, datafile):
		assert MassSpecDataReader(datafile)

		with pytest.raises(IOError, match=r"File not found: i_dont_exist.d\\AcqData\\Contents.xml"):
			MassSpecDataReader("i_dont_exist.d")

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
				'Min Range',
				'TOF Vac',
				'Quad Vac',
				'Rough Vac',
				'PMT',
				'Drying Gas',
				'Gas Temp',
				'Nebulizer',
				'Fragmentor:1',
				'Fragmentor:2',
				'Fragmentor:3',
				'Fragmentor:4',
				'Skimmer(Hex Exit Lens):1',
				'Skimmer(Hex Exit Lens):2',
				'Skimmer(Hex Exit Lens):3',
				'Skimmer(Hex Exit Lens):4',
				'Oct 1 RF Vpp:1',
				'Oct 1 RF Vpp:2',
				'Oct 1 RF Vpp:3',
				'Oct 1 RF Vpp:4',
				'VCap:1',
				'VCap:2',
				'VCap:3',
				'VCap:4',
				'Oct1 DC',
				'Lens 1',
				'Lens 2',
				'Lens 2 RF Enable',
				'Lens 2 RF V',
				'Lens 2 RF Ph',
				'Quad AMU',
				'Quad DC',
				'Post Filter DC',
				'Width Gain',
				'Width Offset',
				'Axis Gain',
				'Axis Offset',
				'Col. Cell Gas',
				'Col. Cell Flow',
				'Hex RF',
				'Hex DC Entr',
				'Hex dV',
				'Cell Entr',
				'Cell Exit',
				'Oct2 DC',
				'Oct 2 RF Vpp',
				'Ion Focus',
				'Slicer',
				'Horiz Q',
				'Vert Q',
				'Top Slit',
				'Bot Slit',
				'Pusher',
				'Puller',
				'Puller Offset',
				'Acc Focus',
				'Mirror Front',
				'Mirror Mid',
				'Mirror Back',
				'MCP',
				'Amp Offset',
				'Turbo1 Speed',
				'Turbo2 Speed',
				'Turbo1 Power',
				'Turbo2 Power',
				'Length of Transients',
				'Vaporizor/Sheath Gas Temp',
				'Calibrant Solution',
				'LC Stream',
				'Charging/Nozzle Voltage',
				'Ion Polarity',
				'Col. Cell Energy',
				'Charge State',
				'Corona',
				'Sheath Gas Flow',
				'Number of Transients',
				'Funnel DC',
				'Funnel Delta HP',
				'Funnel Delta LP',
				'Funnel RF HP',
				'Funnel RF LP',
				'Slicer Position',
				'Collision Energy:1',
				'Collision Energy:2',
				'Collision Energy:3',
				'Collision Energy:4',
				'Drift Tube Temperature',
				'Drift Tube Pressure',
				'Drift Tube Entrance Voltage',
				'Drift Tube Exit Voltage',
				'High Pressure Funnel Exit',
				'High Pressure Funnel Delta',
				'High Pressure Funnel RF',
				'HP Funnel Pressure',
				'IM Hex Entrance',
				'IM Hex RF',
				'Non Turbo Pump Speed',
				'Rear Funnel Entrance',
				'Rear Funnel Exit',
				'Rear Funnel RF',
				'Trap Entrance',
				'Trap Entrance Grid Delta',
				'Trap Entrance Grid Low',
				'Trap Exit',
				'Trap Exit Grid 1 Delta',
				'Trap Exit Grid 1 Low',
				'Trap Exit Grid 2 Delta',
				'Trap Exit Grid 2 Low',
				'Trap Funnel Delta',
				'Trap Funnel Exit',
				'Trap Funnel Pressure',
				'Trap Funnel RF',
				'Turbo Pump Power',
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

		file_regression.check(json.dumps(dict(actuals)), encoding="UTF-8", extension=".json")

	def test_get_sample_data_all(self, reader, file_regression: FileRegressionFixture):
		self.check_json_regression(reader.get_sample_data(), file_regression)

	def test_get_sample_data_unspecified(self, reader, file_regression: FileRegressionFixture):
		self.check_json_regression(reader.get_sample_data(SampleCategory.Unspecified), file_regression)

	def test_get_sample_data_general(self, reader, file_regression: FileRegressionFixture):
		self.check_json_regression(reader.get_sample_data(SampleCategory.General), file_regression)

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
		file_regression.check(
				json.dumps(obj, **kwargs),
				extension=".json",
				encoding="UTF-8",
				)

	def check_signal_regression(self, signals: List[SignalInfo], file_regression: FileRegressionFixture):
		self.check_json_regression(
				[signal.freeze().to_dict() for signal in signals],
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
		signal = reader.get_signal_listing("HiP-ALS", DeviceType.AutoSampler, StoredDataType.InstrumentCurves,)[0].freeze()

		assert FrozenSignalInfo.from_dict(signal.to_dict()) == signal
		assert FrozenSignalInfo.from_dict(json.loads(json.dumps(signal.to_dict()))) == signal


	# get_scan_record
	# get_signal_listing
	# get_spectrum_by_time
	# get_spectrum_by_scan
