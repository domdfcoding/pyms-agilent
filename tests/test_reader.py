# stdlib
import pathlib
import sys

# 3rd party
import pytest
from pyms.GCMS.Class import GCMS_data
from pytest_regressions.data_regression import DataRegressionFixture
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from pyms_agilent.metadata import is_datafile
from pyms_agilent.reader import agilent_reader

pytestmark = pytest.mark.skipif(condition=sys.platform != "win32", reason="Only supported on Windows.")


@pytest.fixture(scope="session")
def datafile():
	file = pathlib.Path(__file__).parent / "example1.d"
	assert file.is_dir()
	assert is_datafile(file)

	return file


@pytest.fixture(scope="module")
def data(datafile) -> GCMS_data:
	return agilent_reader(datafile)


def test_len(data):
	assert len(data) == 1333


def test_info(data, capsys):
	data.info()

	assert capsys.readouterr().out.splitlines() == [
			" Data retention time range: 0.001 min -- 0.250 min",
			" Time step: 0.011 s (std=0.000 s)",
			" Number of scans: 1333",
			" Minimum m/z measured: 40.001",
			" Maximum m/z measured: 999.194",
			" Mean number of m/z values per scan: 5771",
			" Median number of m/z values per scan: 6000",
			]


# TODO: scan_list


def test_time_list(data, data_regression: DataRegressionFixture):
	data_regression.check(data.time_list)


def test_tic(data, data_regression: DataRegressionFixture):
	data_regression.check(data.tic.intensity_array.tolist())


def test_min_rt(data):
	assert data.min_rt == 0.047216666666666664


def test_max_rt(data):
	assert data.max_rt == 14.99765


def test_time_step(data):
	assert data.time_step == 0.01122404904904905


def test_time_step_std(data):
	assert data.time_step_std == 9.0986234621143e-06


@pytest.mark.parametrize("filename", [
		"agilent_data.I.csv",
		"agilent_data.mz.csv",
		])
def test_write(tmpdir, data, file_regression: FileRegressionFixture, filename):
	tmpdir_p = pathlib.Path(tmpdir)
	data.write(tmpdir_p / "agilent_data")
	assert (tmpdir_p / filename).is_file()

	file_regression.check((tmpdir_p / filename).read_text())


def test_write_intensities_stream(tmpdir, data, file_regression: FileRegressionFixture):
	tmpdir_p = pathlib.Path(tmpdir)
	data.write_intensities_stream(tmpdir_p / "agilent_data.dat")
	assert (tmpdir_p / "agilent_data.dat").is_file()

	file_regression.check((tmpdir_p / "agilent_data.dat").read_text())
