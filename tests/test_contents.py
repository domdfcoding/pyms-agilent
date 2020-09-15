# stdlib
import datetime
import pathlib

# this package
from pyms_agilent.enums import AcqStatusEnum, MeasurementTypeEnum, SeparationTechniqueEnum
from pyms_agilent.xml_parser.contents import Contents, read_contents_xml


class TestContents:

	the_datetime = datetime.datetime(
			year=2019,
			month=9,
			day=9,
			hour=12,
			minute=14,
			second=36,
			tzinfo=datetime.timezone.utc,
			)

	def test_from_xml_file(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("MJA5_1000_090919_001.d")

		contents = Contents.from_xml_file(datafile / "AcqData" / "Contents.xml")
		assert isinstance(contents, Contents)

		assert contents.version == 3
		assert contents.acquired_time == self.the_datetime

		assert isinstance(contents.acq_status, AcqStatusEnum)
		assert isinstance(contents.acq_status, int)
		assert contents.acq_status == AcqStatusEnum.End
		assert contents.acq_status == 2

		assert contents.instrument_name == "Instrument 1"

		assert not contents.locked_mode

		assert isinstance(contents.measurement_type, MeasurementTypeEnum)
		assert isinstance(contents.measurement_type, int)
		assert contents.measurement_type == 0
		assert contents.measurement_type == MeasurementTypeEnum.Unknown

		assert isinstance(contents.separation_technique, SeparationTechniqueEnum)
		assert isinstance(contents.separation_technique, int)
		assert contents.separation_technique == 3
		assert contents.separation_technique == SeparationTechniqueEnum.LC

		assert contents.total_run_duration == datetime.timedelta(seconds=816.2)
		assert contents.acq_software_version == "6200 series TOF/6500 series Q-TOF B.09.00 (B9044.1 SP1)"

	def test_read_contents_xml(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		assert isinstance(read_contents_xml(datafile / "AcqData"), Contents)

	def test_creation(self):
		contents = Contents(
				version=1,
				acquired_time="2019-09-09T13:14:36.9085672+01:00",
				acq_status=1,
				instrument_name="The Instrument",
				locked_mode=True,
				measurement_type=2,
				separation_technique=4,
				total_run_duration=17,
				)

		assert contents.version == 1
		assert contents.acquired_time == self.the_datetime

		assert isinstance(contents.acq_status, AcqStatusEnum)
		assert isinstance(contents.acq_status, int)
		assert contents.acq_status == AcqStatusEnum.Start
		assert contents.acq_status == 1

		assert contents.instrument_name == "The Instrument"

		assert contents.locked_mode

		assert isinstance(contents.measurement_type, MeasurementTypeEnum)
		assert isinstance(contents.measurement_type, int)
		assert contents.measurement_type == 2
		assert contents.measurement_type == MeasurementTypeEnum.Chromatographic

		assert isinstance(contents.separation_technique, SeparationTechniqueEnum)
		assert isinstance(contents.separation_technique, int)
		assert contents.separation_technique == 4
		assert contents.separation_technique == SeparationTechniqueEnum.CE

		assert contents.total_run_duration == datetime.timedelta(seconds=17)
		assert contents.acq_software_version == ''

		contents = Contents(
				version="1",  # type: ignore
				acquired_time=datetime.datetime(
						year=2019, month=9, day=9, hour=12, minute=14, second=36, tzinfo=datetime.timezone.utc
						),
				acq_status=AcqStatusEnum.Start,
				instrument_name="The Instrument",
				locked_mode=False,
				measurement_type=MeasurementTypeEnum.Chromatographic,
				separation_technique=SeparationTechniqueEnum.Unspecified,
				total_run_duration=datetime.timedelta(hours=17),
				)

		assert contents.version == 1
		assert contents.acquired_time == self.the_datetime

		assert isinstance(contents.acq_status, AcqStatusEnum)
		assert isinstance(contents.acq_status, int)
		assert contents.acq_status == AcqStatusEnum.Start
		assert contents.acq_status == 1

		assert contents.instrument_name == "The Instrument"

		assert not contents.locked_mode

		assert isinstance(contents.measurement_type, MeasurementTypeEnum)
		assert isinstance(contents.measurement_type, int)
		assert contents.measurement_type == 2
		assert contents.measurement_type == MeasurementTypeEnum.Chromatographic

		assert isinstance(contents.separation_technique, SeparationTechniqueEnum)
		assert isinstance(contents.separation_technique, int)
		assert contents.separation_technique == 0
		assert contents.separation_technique == SeparationTechniqueEnum.Unspecified

		assert contents.total_run_duration == datetime.timedelta(hours=17)
		assert contents.acq_software_version == ''

	def test_dict(self):
		contents = Contents(
				version=1,
				acquired_time="2019-09-09T13:14:36.9085672+01:00",
				acq_status=1,
				instrument_name="The Instrument",
				locked_mode=True,
				measurement_type=2,
				separation_technique=4,
				total_run_duration=17,
				)

		acq_time = datetime.datetime(
				year=2019,
				month=9,
				day=9,
				hour=12,
				minute=14,
				second=36,
				tzinfo=datetime.timezone.utc,
				)

		assert dict(contents) == {
				"version": 1,
				"acquired_time": acq_time,
				"acq_status": AcqStatusEnum.Start,
				"instrument_name": "The Instrument",
				"locked_mode": True,
				"measurement_type": MeasurementTypeEnum.Chromatographic,
				"separation_technique": SeparationTechniqueEnum.CE,
				"total_run_duration": datetime.timedelta(seconds=17),
				"acq_software_version": '',
				}
