import json

from pyms_agilent.enums import ChromType, DataUnit, DataValueType, DeviceType, StoredDataType
from pyms_agilent.mhdac.chromatograms import FrozenInstrumentCurve


def test_equality(reader, datadir):
	signal = reader.get_signal_listing(
			"HiP-ALS",
			DeviceType.AutoSampler,
			StoredDataType.InstrumentCurves,
			)[0]

	curve = signal.get_instrument_curve()

	expected = FrozenInstrumentCurve(
		chromatogram_type=ChromType.Signal,
		device_name="HiP-ALS",
		device_type=DeviceType.AutoSampler,
		is_chromatogram=True,
		is_icp_data=False,
		is_cycle_summed=False,
		is_mass_spectrum=False,
		is_primary_mrm=False,
		is_uv_spectrum=False,
		ordinal_number=1,
		signal_description='Temperature',
		signal_name='A',
		total_data_points=9000,
		x_data=json.loads((datadir / 'x_data.json').read_text()),
		y_data=json.loads((datadir / 'y_data.json').read_text()),
		x_axis_info=(DataValueType.AcqTime, DataUnit.Minutes),
		y_axis_info=(DataValueType.Ordinate, "°C"),
		)

	assert curve.freeze() == expected
	assert curve == expected

	assert expected == curve.freeze()
	assert expected == curve

	assert curve.to_dict() == expected
	assert expected.to_dict() == curve
