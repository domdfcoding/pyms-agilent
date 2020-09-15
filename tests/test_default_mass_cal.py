# stdlib
import pathlib

# this package
from pyms_agilent.enums import CalibrationFormulaEnum, CalibrationTechniqueEnum
from pyms_agilent.xml_parser.default_mass_cal import Calibration, CalibrationList, StepType, read_mass_cal_xml


class TestStepType:

	def test_creation(self):
		step = StepType(1)

		assert step.number == 1
		assert step.calibration_formula == CalibrationFormulaEnum.Undefined
		assert step.calibration_technique == CalibrationTechniqueEnum.Undefined
		assert step.number_of_coefficients == 0
		assert step.value_use_flags == 0
		assert step.values == {}

		step = StepType(
				1,
				calibration_formula=CalibrationFormulaEnum.Traditional,
				calibration_technique=CalibrationTechniqueEnum.ExternalReference,
				number_of_coefficients=7,
				value_use_flags=4
				)

		assert step.number == 1
		assert step.calibration_formula == CalibrationFormulaEnum.Traditional
		assert step.calibration_technique == CalibrationTechniqueEnum.ExternalReference
		assert step.number_of_coefficients == 7
		assert step.value_use_flags == 4
		assert step.values == {}

		step = StepType(1, values={7: 1.234})

		assert step.number == 1
		assert step.calibration_formula == CalibrationFormulaEnum.Undefined
		assert step.calibration_technique == CalibrationTechniqueEnum.Undefined
		assert step.number_of_coefficients == 0
		assert step.value_use_flags == 0
		assert step.values == {7: 1.234}

		step = StepType(1, values={"7": "1.234"})  # type: ignore

		assert step.number == 1
		assert step.calibration_formula == CalibrationFormulaEnum.Undefined
		assert step.calibration_technique == CalibrationTechniqueEnum.Undefined
		assert step.number_of_coefficients == 0
		assert step.value_use_flags == 0
		assert step.values == {7: 1.234}

	def test_dict(self):
		step = StepType(
				1,
				calibration_formula=CalibrationFormulaEnum.Traditional,
				calibration_technique=CalibrationTechniqueEnum.ExternalReference,
				number_of_coefficients=7,
				value_use_flags=4,
				values={7: 1.234},
				)

		assert dict(step) == {
				"number": 1,
				"calibration_formula": CalibrationFormulaEnum.Traditional,
				"calibration_technique": CalibrationTechniqueEnum.ExternalReference,
				"number_of_coefficients": 7,
				"value_use_flags": 4,
				"values": {7: 1.234},
				}


class TestCalibration:

	def test_creation(self):
		cal = Calibration(1)
		assert cal.calibration_id == 1
		assert cal == []

		cal = Calibration("1")  # type: ignore
		assert cal.calibration_id == 1
		assert cal == []

		step = StepType(
				1,
				calibration_formula=CalibrationFormulaEnum.Traditional,
				calibration_technique=CalibrationTechniqueEnum.ExternalReference,
				number_of_coefficients=7,
				value_use_flags=4,
				values={7: 1.234},
				)

		cal = Calibration(1, steps=[step])
		assert cal == [step]

		cal = Calibration(1, steps=(step, ))
		assert cal == [step]


class TestCalibrationList:

	def test_from_xml_file(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		cal_list = CalibrationList.from_xml_file(datafile / "AcqData" / "DefaultMassCal.xml")
		assert isinstance(cal_list, CalibrationList)

		assert cal_list.version == 1
		assert isinstance(cal_list[0], Calibration)

		assert cal_list[0].calibration_id == 1
		assert len(cal_list[0]) == 2

		assert cal_list[1].calibration_id == 2
		assert len(cal_list[1]) == 2

		assert isinstance(cal_list[0][0], StepType)
		assert cal_list[0][0].number == 1
		assert cal_list[0][0].calibration_technique == CalibrationTechniqueEnum.ExternalReference
		assert cal_list[0][0].calibration_formula == CalibrationFormulaEnum.Traditional
		assert cal_list[0][0].number_of_coefficients == 2
		assert cal_list[0][0].value_use_flags == 0
		assert cal_list[0][0].values == {
				1: 0.000345776955256969,
				2: 1006.52436760566,
				}

	def test_read_mass_cal_xml(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		assert isinstance(read_mass_cal_xml(datafile / "AcqData"), CalibrationList)

	def test_creation(self):
		cal = CalibrationList(1)
		assert cal.version == 1
		assert cal == []

		cal = CalibrationList("1")  # type: ignore
		assert cal.version == 1
		assert cal == []
