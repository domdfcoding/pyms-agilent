#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  metadata.py
"""
Extract metadata from Agilent .d datafiles
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
#  is_datafile based on ms_deisotope
#  https://github.com/mobiusklein/ms_deisotope/blob/master/ms_deisotope/data_source/_vendor/AgilentD.py
#  Copyright Joshua Klein
#  Apache 2.0 Licensed
#

# stdlib
import os
import pathlib
from typing import Dict

# 3rd party
from domdf_python_tools.typing import PathLike
from typing_extensions import TypedDict

# this package
from pyms_agilent.xml_parser.acq_method import AcqMethod, read_acqmethod
from pyms_agilent.xml_parser.contents import Contents, read_contents_xml
from pyms_agilent.xml_parser.default_mass_cal import CalibrationList, read_mass_cal_xml
from pyms_agilent.xml_parser.device_config_info import DeviceConfigInfo, read_device_config_xml
from pyms_agilent.xml_parser.devices import DeviceList, read_devices_xml
from pyms_agilent.xml_parser.ms_actual_defs import ActualsDef, read_ms_actuals_defs
from pyms_agilent.xml_parser.ms_time_segments import MSTimeSegments, read_msts_xml
from pyms_agilent.xml_parser.sample_info import SampleInfo, read_sample_info_xml


def prepare_filepath(file_name: PathLike, mkdirs: bool = True) -> pathlib.Path:
	"""
	Convert a filename string into a :class:`pathlib.Path` object, and create parent directories if required.

	:param file_name: file_name to process
	:param mkdirs: Whether the parent directory of the file should be created if it doesn't exist. Default True.

	:return: file_name
	"""

	if not isinstance(file_name, pathlib.Path):
		try:
			file_name = pathlib.Path(file_name)
		except TypeError:
			raise TypeError(f"'file_name' must be a string or a PathLike object, not {type(file_name)}")

	if not file_name.parent.is_dir() and mkdirs:
		file_name.parent.mkdir(parents=True)

	return file_name


MetadataDict = TypedDict(
		"MetadataDict",
		{
				"AcqMethod": AcqMethod,
				"Contents": Contents,
				"DefaultMassCal": CalibrationList,
				"DeviceConfigInfo": DeviceConfigInfo,
				"Devices": DeviceList,
				"MSActualDefs": ActualsDef,
				"MSTS": MSTimeSegments,
				"sample_info": SampleInfo,
				}
		)
"""
:class:`typing.TypedDict` representing the dictionary returned by :func:`.~extract_metadata`.
"""


def extract_metadata(file_name: PathLike) -> MetadataDict:
	"""
	Extract metadata from an Agilent .d datafile

	:param file_name: name of the .d datafile
	"""

	file_name = prepare_filepath(file_name)

	if not is_datafile(file_name):
		raise ValueError(f"'{file_name}' does not appear to be a valid .d datafile.")

	acqdata_dir = file_name / "AcqData"

	return {
			"AcqMethod": read_acqmethod(acqdata_dir),
			"Contents": read_contents_xml(acqdata_dir),
			"DefaultMassCal": read_mass_cal_xml(acqdata_dir),
			"DeviceConfigInfo": read_device_config_xml(acqdata_dir),
			"Devices": read_devices_xml(acqdata_dir),
			"MSActualDefs": read_ms_actuals_defs(acqdata_dir),
			"MSTS": read_msts_xml(acqdata_dir),
			"sample_info": read_sample_info_xml(acqdata_dir),
			}


def is_datafile(file_name: PathLike) -> bool:
	"""
	Returns whether the given path is a valid data file

	:param file_name: name of the .d datafile
	"""

	if not isinstance(file_name, pathlib.Path):
		try:
			file_name = pathlib.Path(file_name)
		except TypeError:
			raise TypeError(f"'file_name' must be a string or a PathLike object, not {type(file_name)}")

	if file_name.exists():
		if file_name.is_dir():
			if ((file_name / "AcqData") / "Contents.xml").exists():
				return True

	return False
