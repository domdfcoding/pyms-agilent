#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  ms_time_segments.py
"""
Parser for mass spectrometry time segment data in MSTS.xml
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
from typing import List, Optional, Union

# 3rd party
import attr
import importlib_resources
import lxml.objectify
from domdf_python_tools.utils import strtobool
from mh_utils.utils import add_attrs_doc

# this package
from . import agilent_xsd
from .core import XMLList


@add_attrs_doc
@attr.s(slots=True)
class TimeSegment:
	"""
	Represents a time segment from ``MSTS.xml``

	:param timesegment_id:
	:param start_time: start time in minutes
	:param end_time: end time in minutes
	:param n_scans:
	:param fixed_cycle_length:
	"""

	def __make_start_timedelta(self, the_attr: attr.Attribute, the_value):
		if not isinstance(self.start_time, datetime.timedelta):
			self.start_time = datetime.timedelta(minutes=float(self.start_time))

	def __make_end_timedelta(self, the_attr: attr.Attribute, the_value):
		if not isinstance(self.end_time, datetime.timedelta):
			self.end_time = datetime.timedelta(minutes=float(self.end_time))

	timesegment_id: int = attr.ib(converter=int)
	start_time: Union[float, datetime.timedelta] = attr.ib(validator=__make_start_timedelta, default=0.0)
	end_time: Union[float, datetime.timedelta] = attr.ib(validator=__make_end_timedelta, default=0.0)
	n_scans: int = attr.ib(converter=int, default=0)
	fixed_cycle_length: bool = attr.ib(converter=strtobool, default=False)

	@classmethod
	def from_xml(cls, element):

		return cls(
				timesegment_id=element.attrib["TimeSegmentID"],
				start_time=element.StartTime,
				end_time=element.EndTime,
				n_scans=element.NumOfScans,
				fixed_cycle_length=str(element.FixedCycleLength),
				)


class MSTimeSegments(XMLList):
	"""
	Represents the list of MS time segments from ``MSTS.xml``.

	:param version:
	:param irm_status:
	:param time_segments:
	:type time_segments:
	"""

	def __init__(self, version: int, irm_status: int = 0, time_segments: Optional[List[TimeSegment]] = None):
		super().__init__(version, time_segments)

		self.irm_status = int(irm_status)

	_content_type = TimeSegment
	_content_xml_name = "TimeSegment"

	with importlib_resources.path(agilent_xsd, "MSTS.xsd") as path:
		_schema = str(path)

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "MSTimeSegments":
		"""
		Construct an :class:`~.MSTS` object from an XML element.

		:param element: The XML element to parse the data from
		"""

		version = int(element.Version)  # sample_info version number

		obj = cls(version, irm_status=element.IRMStatus)
		obj._append_from_element(element)
		return obj


def read_msts_xml(base_path) -> "MSTimeSegments":
	"""
	Construct an an :class:`~.MSTS` object from the ``sample_info.xml`` file in the given directory.

	:param base_path:
	"""

	return MSTimeSegments.from_xml_file(pathlib.Path(base_path) / "MSTS.xml")
