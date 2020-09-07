#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  contents.py
"""
Parser for Contents.xml
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
import datetime
import pathlib
from typing import Union

# 3rd party
import importlib_resources
import lxml.objectify  # type: ignore
from domdf_python_tools.bases import Dictable
from domdf_python_tools.typing import PathLike
from mh_utils.utils import element_to_bool
from mh_utils.worklist_parser.parser import parse_worklist_datetime

# this package
from pyms_agilent.xml_parser import agilent_xsd

# this package
from .core import XMLFileMixin, _get_from_enum
from pyms_agilent.enums import AcqStatusEnum, MeasurementTypeEnum, SeparationTechniqueEnum

__all__ = ["Contents", "read_contents_xml"]


class Contents(XMLFileMixin, Dictable):
	"""
	Represents the contents of the ``.d`` datafile, parsed from ``Contents.xml``.

	:param version: The version number of the contents file.
	:param acquired_time: The acquisition time
	:param acq_status:
	:param instrument_name: The name of the instrument
	:param locked_mode:
	:param measurement_type:
	:param separation_technique: The separation technique used
	:param total_run_duration: The total time taken for acquisition in seconds
	:param acq_software_version: The version number of the software that acquired the data.
	"""

	def __init__(
			self,
			version: int,
			acquired_time: Union[str, datetime.datetime],
			acq_status: Union[AcqStatusEnum, int],
			instrument_name: str = '',
			locked_mode: bool = False,
			measurement_type: Union[MeasurementTypeEnum, int] = 0,
			separation_technique: Union[SeparationTechniqueEnum, int] = 0,
			total_run_duration: Union[float, datetime.timedelta] = 0.0,
			acq_software_version: str = ''
			):
		super().__init__()

		self.version = int(version)

		if isinstance(acquired_time, datetime.datetime):
			self.acquired_time = acquired_time
		else:
			self.acquired_time = parse_worklist_datetime(acquired_time)

		self.acq_status = _get_from_enum(acq_status, AcqStatusEnum, int)
		self.instrument_name = str(instrument_name)
		self.locked_mode = bool(locked_mode)
		self.measurement_type = _get_from_enum(measurement_type, MeasurementTypeEnum, int)
		self.separation_technique = _get_from_enum(separation_technique, SeparationTechniqueEnum, int)

		if isinstance(total_run_duration, datetime.timedelta):
			self.total_run_duration = total_run_duration
		else:
			self.total_run_duration = datetime.timedelta(seconds=float(total_run_duration))

		self.acq_software_version = str(acq_software_version)

	__slots__ = [
			"version",
			"acquired_time",
			"acq_status",
			"instrument_name",
			"locked_mode",
			"measurement_type",
			"separation_technique",
			"total_run_duration",
			"acq_software_version",
			]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	with importlib_resources.path(agilent_xsd, "Contents.xsd") as schema_path:
		_schema = str(schema_path)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "Contents":
		"""
		Construct a :class:`~.Contents` object from an XML element.

		:param element: The XML element to parse the data from.
		"""

		return cls(
				version=element.Version,
				acquired_time=element.AcquiredTime,
				acq_status=element.AcqStatus,
				instrument_name=element.InstrumentName,
				locked_mode=element_to_bool(element.LockedMode),
				measurement_type=element.MeasurementType,
				separation_technique=element.SeparationTechnique,
				total_run_duration=element.TotalRunDuration,
				acq_software_version=element.AcqSoftwareVersion,
				)


def read_contents_xml(base_path: PathLike) -> Contents:
	"""
	Construct a :class:`~.Contents` object from the ``Contents.xml`` file in the given directory.

	:param base_path:
	"""

	return Contents.from_xml_file(pathlib.Path(base_path) / "Contents.xml")
