import json
from textwrap import dedent

import pytest

from pyms_agilent.enums import (
	DataUnit, DataValueType, DeviceType, IonizationMode, MSLevel, MSScanType, MSStorageMode,
	SpecType,
	)
from pyms_agilent.exceptions import NotMS2Error
from pyms_agilent.mhdac.spectrum import FrozenSpecData
from pyms_agilent.utils import Range


@pytest.fixture(scope="function")
def spectrum(reader):
	return reader.get_spectrum_by_scan(0)


@pytest.fixture(scope="function")
def frozen_spectrum(datadir):
	return FrozenSpecData(
				abundance_limit=16742400.0,
				acquired_time_ranges=[Range(0.047216666666666664, 0.047216666666666664)],
				chrom_peak_index=-1,
				collision_energy=0.0,
				compensation_field=float('nan'),
				device_name="QTOF",
				device_type=DeviceType.QuadrupoleTimeOfFlight,
				dispersion_field=float('nan'),
				fragmentor_voltage=380.0,
				x_axis_info=(DataValueType.MassToCharge, DataUnit.Thomsons),
				y_axis_info=(DataValueType.IonAbundance, DataUnit.Counts),
				ionization_polarity="+",
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
				x_data=json.loads((datadir / 'x_data.json').read_text()),
				y_data=json.loads((datadir / 'y_data.json').read_text()),
				)




class TestSpecData:

	def test_repr(self, spectrum):
		assert repr(spectrum) == dedent("""\
		pyms_agilent.mhdac.spectrum.SpecData(
			abundance_limit=16742400.0,
			acquired_time_ranges=[
				pyms_agilent.utils.Range(
					start=0.047216666666666664,
					stop=0.047216666666666664
				)
			],
			chrom_peak_index=-1,
			collision_energy=0.0,
			compensation_field=float('nan'),
			device_name='QTOF',
			device_type=<DeviceType.QuadrupoleTimeOfFlight: 6>,
			dispersion_field=float('nan'),
			fragmentor_voltage=380.0,
			x_axis_info=(<DataValueType.MassToCharge: 5>, <DataUnit.Thomsons: 10>),
			y_axis_info=(<DataValueType.IonAbundance: 15>, <DataUnit.Counts: 16>),
			ionization_polarity='+',
			ionization_mode=<IonizationMode.ESI: 64>,
			is_chromatogram=False,
			is_data_in_mass_unit=True,
			is_mass_spectrum=True,
			is_icp_data=False,
			is_uv_spectrum=False,
			ms_level=<MSLevel.MS: 1>,
			ms_scan_type=<MSScanType.Scan: 1>,
			ms_storage_mode=<MSStorageMode.PeakDetectedSpectrum: 3>,
			mz_of_interest=[],
			measured_mass_range=pyms_agilent.utils.Range(
				start=40.05473406265757,
				stop=999.1105542357848
			),
			ordinal_number=1,
			parent_scan_id=0,
			sampling_period=0.5,
			scan_id=2841,
			spectrum_type=<SpecType.TofMassSpectrum: 3>,
			threshold=0.0,
			total_data_points=6000,
			total_scan_count=1,
			x_data=[
				40.05473406265757,
				40.185835251503065,
				40.22438556140809,
				40.27292880849117,
				40.31492688232336,
				40.35732021803396,
				40.449253771099855,
				40.58728484859273,
				40.60232628956523,
				40.625960629446176,
				...
			],
			y_data=[
				850.64,
				683.0417,
				826.1984,
				1073.483,
				714.449,
				704.889,
				759.8514,
				664.7151,
				658.0245,
				748.1315,
				...
			]
		)""").expandtabs(4)


class TestFrozenSpecData:

	def test_repr(self, frozen_spectrum):

		assert repr(frozen_spectrum) == dedent("""\
		pyms_agilent.mhdac.spectrum.FrozenSpecData(
			abundance_limit=16742400.0,
			acquired_time_ranges=[
				pyms_agilent.utils.Range(
					start=0.047216666666666664,
					stop=0.047216666666666664
				)
			],
			chrom_peak_index=-1,
			collision_energy=0.0,
			compensation_field=float('nan'),
			device_name='QTOF',
			device_type=<DeviceType.QuadrupoleTimeOfFlight: 6>,
			dispersion_field=float('nan'),
			fragmentor_voltage=380.0,
			x_axis_info=(<DataValueType.MassToCharge: 5>, <DataUnit.Thomsons: 10>),
			y_axis_info=(<DataValueType.IonAbundance: 15>, <DataUnit.Counts: 16>),
			ionization_polarity='+',
			ionization_mode=<IonizationMode.ESI: 64>,
			is_chromatogram=False,
			is_data_in_mass_unit=True,
			is_mass_spectrum=True,
			is_icp_data=False,
			is_uv_spectrum=False,
			ms_level=<MSLevel.MS: 1>,
			ms_scan_type=<MSScanType.Scan: 1>,
			ms_storage_mode=<MSStorageMode.PeakDetectedSpectrum: 3>,
			mz_of_interest=[],
			measured_mass_range=pyms_agilent.utils.Range(
				start=40.05473406265757,
				stop=999.1105542357848
			),
			ordinal_number=1,
			parent_scan_id=0,
			sampling_period=0.5,
			scan_id=2841,
			spectrum_type=<SpecType.TofMassSpectrum: 3>,
			threshold=0.0,
			total_data_points=6000,
			total_scan_count=1,
			x_data=[
				40.05473406265757,
				40.185835251503065,
				40.22438556140809,
				40.27292880849117,
				40.31492688232336,
				40.35732021803396,
				40.449253771099855,
				40.58728484859273,
				40.60232628956523,
				40.625960629446176,
				...
			],
			y_data=[
				850.64,
				683.0417,
				826.1984,
				1073.483,
				714.449,
				704.889,
				759.8514,
				664.7151,
				658.0245,
				748.1315,
				...
			]
		)""").expandtabs(4)

	def test_not_ms2(self, frozen_spectrum):
		with pytest.raises(NotMS2Error):
			frozen_spectrum.precursor_charge

		with pytest.raises(NotMS2Error):
			frozen_spectrum.precursor_intensity
