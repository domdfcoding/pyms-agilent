# stdlib
import pathlib

# 3rd party
import lxml.objectify  # type: ignore
import pytest

# this package
from pyms_agilent.xml_parser.acq_method import AcqMethod, Device, read_acqmethod, tag2dict


def test_from_xml_file(monkeypatch):
	monkeypatch.chdir(pathlib.Path(__file__).parent)
	datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

	method = AcqMethod.from_xml_file(datafile / "AcqData" / "AcqMethod.xml")

	assert isinstance(method, AcqMethod)

	assert isinstance(method.version, float)
	assert method.version == 5.0

	assert isinstance(method.name, str)
	assert method.name == "Benito Gunshot Residue Positive.m"

	assert isinstance(method.filename, pathlib.Path)
	assert method.filename == pathlib.Path(
			r"D:\MassHunter\Methods\Dominic Davis-Foster\Benito Gunshot Residue Positive.m"
			)

	assert isinstance(method.devices, list)
	assert isinstance(method.devices[0], Device)

	assert method.devices[0].device_id == "HiP-ALS_1"
	assert method.devices[0].display_name == "Multisampler"
	assert method.devices[0].rc_device is True


def test_read_acqmethod(monkeypatch):
	monkeypatch.chdir(pathlib.Path(__file__).parent)
	datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

	assert isinstance(read_acqmethod(datafile / "AcqData"), AcqMethod)


class TestCreation:

	@pytest.mark.parametrize("value, expects", [
			("1.2", 1.2),
			("1", 1.0),
			(1, 1.0),
			(1.2, 1.2),
			])
	def test_version(self, value, expects):
		assert AcqMethod(value, "the name", "method.m").version == expects

	@pytest.mark.parametrize(
			"value, expects",
			[
					("method.m", pathlib.Path("method.m")),
					(pathlib.Path("method.m"), pathlib.Path("method.m")),
					(pathlib.Path("directory/method.m"), pathlib.Path("directory/method.m")),
					("directory/method.m", pathlib.Path("directory/method.m")),
					],
			)
	def test_filename(self, value, expects):
		assert AcqMethod(1.0, "the name", value).filename == expects


def test_dict():

	method = AcqMethod(1.0, "the name", "method.m")

	assert dict(method) == dict(
			version=1.0,
			name="the name",
			filename=pathlib.Path("method.m"),
			devices=[],
			)


def test_tag2dict():
	element = lxml.objectify.Element("Fruits")
	element.Apple = 123
	element.Orange = 12.34
	element.Strawberry = "abcdefg"
	element.GrannySmith = "delicious"
	element.Grapes = None

	assert tag2dict(element) == {
			"apple": 123,
			"orange": 12.34,
			"strawberry": "abcdefg",
			"granny_smith": "delicious",
			"grapes": None,
			}

	element = lxml.objectify.Element("Fruits")
	element.Apple = 123
	element.Orange = 12.34
	element.Strawberry = "abcdefg"
	element.GrannySmith = "delicious"
	element.Grapes = None

	assert tag2dict(
			element, camel_lookup={"GrannySmith": "granny smith"}
			) == {
					"apple": 123,
					"orange": 12.34,
					"strawberry": "abcdefg",
					"granny smith": "delicious",
					"grapes": None,
					}
