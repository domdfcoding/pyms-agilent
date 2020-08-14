# stdlib
import datetime
import pathlib

# this package
from pyms_agilent.xml_parser.default_mass_cal import Calibration, CalibrationList, read_mass_cal_xml
from pyms_agilent.xml_parser.device_config_info import Device, DeviceConfigInfo, Parameter, read_device_config_xml
from pyms_agilent.xml_parser.enums import (
		AcqStatusEnum,
		CalibrationFormulaEnum,
		CalibrationTechniqueEnum,
		MeasurementTypeEnum,
		SeparationTechniqueEnum
		)


def test_device():
	device = Device(device_id="HiP-ALS_1", display_name="Multisampler")

	assert device.device_id == "HiP-ALS_1"
	assert device.display_name == "Multisampler"


class TestParameter:

	def test_creation(self):
		param = Parameter(
				device_id="TCC_1",
				resource_name="ExtendedRunInformation",
				resource_id="RunStart_ValvePosition_Description",
				value="Position 3 (Port 3 -> 3')",
				display_name="Run Start Valve Pos. Desc.",
				)

		assert param.device_id == "TCC_1"
		assert param.resource_name == "ExtendedRunInformation"
		assert param.resource_id == "RunStart_ValvePosition_Description"
		assert param.value == "Position 3 (Port 3 -> 3')"
		assert param.units == ""
		assert param.display_name == "Run Start Valve Pos. Desc."

		param = Parameter(
				device_id="TCC_1",
				resource_name="columntags",
				resource_id="Tag_Content_MaxTemperature",
				value="0",
				units="°C",
				display_name="Tag Max. Temp.",
				)

		assert param.device_id == "TCC_1"
		assert param.resource_name == "columntags"
		assert param.resource_id == "Tag_Content_MaxTemperature"
		assert param.value == "0"
		assert param.units == "°C"
		assert param.display_name == "Tag Max. Temp."

	def test_dict(self):

		param = Parameter(
				device_id="TCC_1",
				resource_name="columntags",
				resource_id="Tag_Content_MaxTemperature",
				value="0",
				units="°C",
				display_name="Tag Max. Temp.",
				)

		assert dict(param) == {
				"device_id": "TCC_1",
				"resource_name": "columntags",
				"resource_id": "Tag_Content_MaxTemperature",
				"value": "0",
				"units": "°C",
				"display_name": "Tag Max. Temp.",
				}

	def test_repr(self):
		param = Parameter(
				device_id="TCC_1",
				resource_name="columntags",
				resource_id="Tag_Content_MaxTemperature",
				value="0",
				units="°C",
				display_name="Tag Max. Temp.",
				)

		assert repr(param) == f"<Parameter(Tag Max. Temp.)>"


class TestDeviceConfigInfo:

	def test_from_xml_file(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		config = DeviceConfigInfo.from_xml_file(datafile / "AcqData" / "DeviceConfigInfo.xml")
		assert isinstance(config, DeviceConfigInfo)

		assert isinstance(config.parameters, list)
		assert len(config.parameters) == 44
		assert config.parameters[0].device_id == "TCC_1"
		assert config.parameters[0].resource_name == "ExtendedRunInformation"
		assert config.parameters[0].resource_id == "RunStart_ValvePosition_Description"
		assert config.parameters[0].value == "Position 3 (Port 3 -> 3')"
		assert config.parameters[0].units == ""
		assert config.parameters[0].display_name == "Run Start Valve Pos. Desc."

		assert isinstance(config.devices, list)
		assert len(config.devices) == 3
		assert config.devices[0].device_id == "TCC_1"
		assert config.devices[0].display_name == "Column Comp."

	def test_read_config_xml(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		assert isinstance(read_device_config_xml(datafile / "AcqData"), DeviceConfigInfo)

	def test_creation(self):

		config = DeviceConfigInfo([], [])
		assert isinstance(config.parameters, list)
		assert isinstance(config.devices, list)

		config = DeviceConfigInfo((), ())
		assert isinstance(config.parameters, list)
		assert isinstance(config.devices, list)

	def test_dict(self):
		config = DeviceConfigInfo([], [])

		assert dict(config) == {
				"parameters": [],
				"devices": [],
				}
