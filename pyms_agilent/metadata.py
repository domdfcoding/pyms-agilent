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


# stdlib
import os
import pathlib

# this package
from pyms_agilent.xml_parser.Contents import read_contents_xml
from pyms_agilent.xml_parser.DefaultMassCal import read_mass_cal_xml
from pyms_agilent.xml_parser.DeviceConfigInfo import read_device_config_xml
from pyms_agilent.xml_parser.Devices import read_devices_xml
from pyms_agilent.xml_parser.MSActualDefs import read_ms_actuals_defs
from pyms_agilent.xml_parser.MSTS import read_msts_xml
from pyms_agilent.xml_parser.sample_info import read_sample_info_xml


_path_types = (str, os.PathLike, pathlib.Path)


def prepare_filepath(file_name, mkdirs=True):
	"""
	Convert string filename into pathlib.Path object and create parent directories if required

	:param file_name: file_name to process
	:type file_name: str or os.PathLike
	:param mkdirs: Whether the parent directory of the file should be created if it doesn't exist. Default True.
	:type mkdirs: bool, optional

	:return: file_name
	:rtype: pathlib.Path

	:author: Dominic Davis-Foster
	"""

	if not isinstance(file_name, pathlib.Path):
		try:
			file_name = pathlib.Path(file_name)
		except TypeError:
			raise TypeError(f"'file_name' must be a string or a PathLike object, not {type(file_name)}")

	if not file_name.parent.is_dir() and mkdirs:
		file_name.parent.mkdir(parents=True)

	return file_name


def is_path(obj):
	"""
	Returns whether the object represents a filesystem path

	:param obj:
	:type obj:

	:return:
	:rtype:
	"""

	if isinstance(obj, _path_types):
		return True
	else:
		return hasattr(obj, " __fspath__")


def extract_metadata(file_name):
	"""
	Extract metadata from an Agilent .d datafile

	:param file_name: name of the .d datafile
	:type file_name: str or os.PathLike
	"""

	if not is_path(file_name):
		raise TypeError("'file_name' must be a string or a PathLike object")

	file_name = prepare_filepath(file_name)

	if not is_datafile(file_name):
		raise ValueError(f"'{file_name}' does not appear to be a valid .d datafile.")

	acqdata_dir = file_name / "AcqData"

	# print(dict(read_contents_xml(acqdata_dir)))
	# print((read_mass_cal_xml(acqdata_dir)))
	# print(dict(read_device_config_xml(acqdata_dir)))
	# print(read_devices_xml(acqdata_dir).to_dict())
	# print(read_ms_actuals_defs(acqdata_dir))
	# print(read_msts_xml(acqdata_dir))
	# print(read_sample_info_xml(acqdata_dir))

	device_configuration = read_device_config_xml(acqdata_dir)
	print(device_configuration.devices)
	print(device_configuration.parameters)
	for param in device_configuration.parameters:
		if param.DisplayName == "Tune Mass Range Max.":
			print(param)
			print(type(param))
			print(param.DisplayName)
			print(param.DisplayName == "Tune Mass Range Max.")
			print(param.Value)
			print(type(param.Value))
			print(param.Units)
			print(type(param.Units))


	# print(dict())



def is_datafile(file_name):
	"""
	Returns whether the given path is a valid data file

	Based on ms_deisotope

	:param file_name: name of the .d datafile
	:type file_name: str or os.PathLike
	"""

	if not is_path(file_name):
		raise TypeError("'file_name' must be a string or a PathLike object")

	file_name = prepare_filepath(file_name)

	if file_name.exists():
		if file_name.is_dir():
			if ((file_name / "AcqData") / "Contents.xml").exists():
				return True
	return False
