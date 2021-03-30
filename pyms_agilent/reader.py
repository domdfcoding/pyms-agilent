#  !/usr/bin/env python
#
#  reader.py
"""
Functions for I/O of data in Agilent ``.d`` format.
"""
#
#  Copyright © 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import pathlib
from statistics import mean

# 3rd party
from domdf_python_tools.typing import PathLike
from pyms.GCMS.Class import GCMS_data  # type: ignore  # TODO
from pyms.Spectrum import Scan  # type: ignore  # TODO

# this package
from pyms_agilent.mhdac.mass_spec_data_reader import MassSpecDataReader

__all__ = ["agilent_reader"]


def agilent_reader(file_name: PathLike) -> GCMS_data:  # pragma: no cover (!Windows)
	"""
	Reader for Agilent MassHunter ``.d`` files.

	:param file_name: Path of the file to read.

	:return: GC-MS data object.
	"""

	if not isinstance(file_name, (str, pathlib.Path)):
		raise TypeError("'file_name' must be a string or a pathlib.Path object")

	if not isinstance(file_name, pathlib.Path):
		file_name = pathlib.Path(file_name)

	print(f" -> Reading Agilent data file '{file_name}'")

	time_list = []
	scan_list = []

	reader = MassSpecDataReader(file_name)

	for scan_no in range(reader.file_information.ms_scan_file_info.total_scans):
		spectrum = reader.get_spectrum_by_scan(scan_no)
		scan_list.append(Scan(spectrum.x_data, spectrum.y_data))
		time_list.append(mean(spectrum.acquired_time_ranges[0]) * 60.0)

	# sanity check
	time_len = len(time_list)
	scan_len = len(scan_list)
	if not time_len == scan_len:  # pragma: no cover
		print(time_list)
		print(scan_list)
		raise ValueError(f"Number of time points ({time_len}) does not equal the number of scans ({scan_len}).")

	data = GCMS_data(time_list, scan_list)

	return data
