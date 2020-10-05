# stdlib
import pathlib
import sys

# 3rd party
import pytest

# this package
from pyms_agilent.metadata import is_datafile
from pyms_agilent.mhdac.file_information import FileInformation
from pyms_agilent.mhdac.mass_spec_data_reader import MassSpecDataReader
from pyms_agilent.mhdac.ms_scan_file_info import MSScanFileInformation

pytest_plugins = "pytest_regressions"

if sys.platform != "win32":
	collect_ignore_glob = ["*.py"]
else:
	import pyms_agilent.mhdac._posix_data_analysis


@pytest.fixture(scope="session")
def datafile():
	file = pathlib.Path(__file__).parent.parent / "example1.d"
	assert file.is_dir()
	assert is_datafile(file)

	return file


@pytest.fixture(scope="session")
def reader(datafile) -> MassSpecDataReader:
	return MassSpecDataReader(datafile)


@pytest.fixture(scope="session")
def file_info(reader) -> FileInformation:
	return reader.file_information


@pytest.fixture(scope="session")
def ms_scan_file_info(reader) -> MSScanFileInformation:
	return reader.file_information.ms_scan_file_info
