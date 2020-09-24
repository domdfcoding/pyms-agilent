#  !/usr/bin/env python
#
#  reader.py
"""
Functions for I/O of data in Agilent ``.d`` format
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

# 3rd party
from domdf_python_tools.typing import PathLike
from pyms.GCMS.Class import GCMS_data
from pyms.Utils.IO import prepare_filepath

# this package
from pyms_agilent.mhdac.mass_spec_data_reader import MassSpecDataReader

__all__ = ["agilent_reader"]


def agilent_reader(file_name: PathLike) -> GCMS_data:
	"""
	Reader for Agilent MassHunter ``.d`` files

	:param file_name: Path of the file to read

	:return: GC-MS data object

	:author: Qiao Wang
	:author: Andrew Isaac
	:author: Vladimir Likic
	:author: Dominic Davis-Foster
	"""

	file_name = prepare_filepath(file_name)

	print(f" -> Reading Agilent data file '{file_name}'")

	reader = MassSpecDataReader(file_name)
	print(reader.file_information.ms_scan_file_info.total_scans)
