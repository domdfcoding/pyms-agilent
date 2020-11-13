# stdlib
import pathlib

# this package
from pyms_agilent.xml_parser.sample_info import Field, SampleInfo, read_sample_info_xml


class TestSampleInfo:

	def test_from_xml_file(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		sample_info = SampleInfo.from_xml_file(datafile / "AcqData" / "sample_info.xml")
		assert isinstance(sample_info, SampleInfo)
		assert isinstance(sample_info[0], Field)
		assert sample_info[0].name == "Sample ID"
		assert sample_info[0].display_name == "Sample ID"
		assert sample_info[0].value == "\n    "
		assert sample_info[0].data_type == 8
		assert sample_info[0].units == ''
		assert sample_info[0].field_type == "SYSTEM"
		assert not sample_info[0].overridden

	def test_read_sample_info(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		assert isinstance(read_sample_info_xml(datafile / "AcqData"), SampleInfo)

	def test_creation(self):
		assert SampleInfo(1).version == 1
		assert SampleInfo('1').version == 1  # type: ignore
