# stdlib
import pathlib

# 3rd party
import pytest
from numpy import float64, int64  # type: ignore

# this package
from pyms_agilent.xml_parser.ms_actual_defs import Actual, ActualsDef, read_ms_actuals_defs


class TestActual:

	def test_creation(self):
		actual = Actual(1)

		assert actual.actual_id == 1
		assert actual.display_name == ''
		assert actual.data_type is float64
		assert actual.display_format == 0
		assert actual.display_effects == 0
		assert actual.display_digits == 0
		assert actual.unit == ''
		assert actual.category == ''

		actual = Actual(
				361,
				display_name="Min Range",
				data_type=4,
				display_format=0,
				display_effects=0,
				display_digits=0,
				unit="nanoSecs",
				category="TOF",
				)

		assert actual.actual_id == 361
		assert actual.display_name == "Min Range"
		assert actual.data_type is int64
		assert actual.display_format == 0
		assert actual.display_effects == 0
		assert actual.display_digits == 0
		assert actual.unit == "nanoSecs"
		assert actual.category == "TOF"

	def test_dict(self):
		actual = Actual(
				361,
				display_name="Min Range",
				data_type=4,
				display_format=0,
				display_effects=0,
				display_digits=0,
				unit="nanoSecs",
				category="TOF",
				)

		assert dict(actual) == {
				"actual_id": 361,
				"display_name": "Min Range",
				"data_type": int64,
				"display_format": 0,
				"display_effects": 0,
				"display_digits": 0,
				"unit": "nanoSecs",
				"category": "TOF",
				}

	@pytest.mark.parametrize(
			"dtype, expects",
			[
					(1, str),
					(2, str),
					(3, str),
					(4, int64),
					(5, str),
					(6, float64),
					(7, str),
					(8, str),
					(9, str),
					(10, str),
					(str, str),
					(int, int),
					(float, float),
					(float64, float64),
					(int64, int64),
					(list, list),
					(tuple, tuple),
					],
			)
	def test_dtypes(self, dtype, expects):
		actual = Actual(
				361,
				display_name="Min Range",
				data_type=dtype,
				display_format=0,
				display_effects=0,
				display_digits=0,
				unit="nanoSecs",
				category="TOF",
				)

		assert actual.data_type is expects

	@pytest.mark.parametrize(
			"actual_id, expects",
			[
					*[(x, float64) for x in range(55)],
					*[(x, int64) for x in range(55, 65)],
					*[(x, float64) for x in range(65, 346)],
					*[(x, int64) for x in range(346, 500)],
					],
			)
	def test_dtypes_guess(self, actual_id, expects):
		actual = Actual(actual_id)
		assert actual.data_type is expects


class TestActualsDef:

	demo_actual = Actual(
			361,
			display_name="Min Range",
			data_type=4,
			display_format=0,
			display_effects=0,
			display_digits=0,
			unit="nanoSecs",
			category="TOF",
			)

	@pytest.mark.parametrize(
			"actual, version, type_, as_list",
			[
					(ActualsDef(1), 1, 0, []),
					(ActualsDef('1'), 1, 0, []),  # type: ignore
					(ActualsDef(1, 1), 1, 1, []),
					(ActualsDef('1', 1), 1, 1, []),  # type: ignore
					(ActualsDef(1, 1, actuals=[demo_actual]), 1, 1, [demo_actual]),
					(ActualsDef('1', 1, actuals=[demo_actual]), 1, 1, [demo_actual]),  # type: ignore
					(ActualsDef(1, 1, actuals=(demo_actual, )), 1, 1, [demo_actual]),
					(ActualsDef('1', 1, actuals=(demo_actual, )), 1, 1, [demo_actual]),  # type: ignore
					(ActualsDef(1, actuals=[demo_actual]), 1, 0, [demo_actual]),
					(ActualsDef('1', actuals=[demo_actual]), 1, 0, [demo_actual]),  # type: ignore
					(ActualsDef(1, actuals=(demo_actual, )), 1, 0, [demo_actual]),
					(ActualsDef('1', actuals=(demo_actual, )), 1, 0, [demo_actual]),  # type: ignore
					],
			)
	def test_creation(self, actual, version, type_, as_list):
		assert actual.version == version
		assert actual.type_ == type_
		assert actual == as_list
		assert list(actual) == as_list

	def test_from_xml_file(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		actuals: ActualsDef = ActualsDef.from_xml_file(datafile / "AcqData" / "MSActualDefs.xml")
		assert isinstance(actuals, ActualsDef)

		assert actuals.version == 1
		assert actuals.type_ == 0
		assert len(actuals) == 118 - 5

		assert isinstance(actuals[0], Actual)

		assert actuals[0] == self.demo_actual

	def test_repr(self):
		assert repr(self.demo_actual) == "<Actual('Min Range', id=361)>"
		assert str(self.demo_actual) == "Min Range"

	def test_read_mass_cal_xml(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		assert isinstance(read_ms_actuals_defs(datafile / "AcqData"), ActualsDef)
