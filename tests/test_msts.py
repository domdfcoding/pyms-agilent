# stdlib
import datetime
import pathlib

# this package
from pyms_agilent.xml_parser.ms_time_segments import MSTimeSegments, TimeSegment, read_msts_xml


class TestMSTS:

	def test_from_xml_file(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("MJA5_1000_090919_001.d")

		ms_time_segments = MSTimeSegments.from_xml_file(datafile / "AcqData" / "MSTS.xml")
		assert isinstance(ms_time_segments, MSTimeSegments)
		assert isinstance(ms_time_segments[0], TimeSegment)
		assert ms_time_segments[0].timesegment_id == 1
		assert ms_time_segments[0].start_time == datetime.timedelta(minutes=0.0520833333333333)
		assert ms_time_segments[0].end_time == datetime.timedelta(minutes=11.9943)
		assert ms_time_segments[0].n_scans == 1065
		assert not ms_time_segments[0].fixed_cycle_length
		assert ms_time_segments.irm_status == 0

		assert len(ms_time_segments) == 1

	def test_read_msts_xml(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		assert isinstance(read_msts_xml(datafile / "AcqData"), MSTimeSegments)

	def test_creation(self):
		assert MSTimeSegments(1).version == 1
		assert MSTimeSegments('1').version == 1  # type: ignore
		assert MSTimeSegments(1, irm_status=1).irm_status == 1
		assert MSTimeSegments(1, irm_status='1').irm_status == 1  # type: ignore
