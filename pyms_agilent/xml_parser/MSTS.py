#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  MSTS.py
"""
Parser for MSTS.xml
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
from collections import namedtuple

# this package
from .core import XMLList


class TimeSegment(namedtuple('__BaseTimeSegment', 'TimeSegmentID StartTime EndTime NumOfScans FixedCycleLength')):
	"""
		
		:param TimeSegmentID:
		:type TimeSegmentID: int
		:param StartTime: start time in minutes
		:type StartTime: float or datetime.timedelta
		:param EndTime: end time in minutes
		:type EndTime: float or datetime.timedelta
		:param NumOfScans:
		:type NumOfScans: int
		:param FixedCycleLength:
		:type FixedCycleLength: bool
		"""
	
	__slots__ = []
	
	def __new__(cls, TimeSegmentID, StartTime=0.0, EndTime=0.0, NumOfScans=0, FixedCycleLength=False):
		
		if not isinstance(StartTime, datetime.timedelta):
			StartTime = datetime.timedelta(minutes=float(StartTime))
			
		if not isinstance(EndTime, datetime.timedelta):
			EndTime = datetime.timedelta(minutes=float(EndTime))
		
		return super().__new__(
				cls,
				TimeSegmentID=int(TimeSegmentID),
				StartTime=StartTime,
				EndTime=EndTime,
				NumOfScans=int(NumOfScans),
				FixedCycleLength=bool(FixedCycleLength),
				)
	
	@classmethod
	def from_xml(cls, element):
		
		TimeSegmentID = element.attrib["TimeSegmentID"]
		
		data = dict(
				StartTime=0.0, EndTime=0.0,
				NumOfScans=0, FixedCycleLength=False
				)
		
		for tag_name in list(data.keys()):
			tag = element.findall(tag_name)
		
			if tag:
				if tag_name == "FixedCycleLength":
					data[tag_name] = int(tag[0].text)
				else:
					data[tag_name] = tag[0].text
				
		return cls(TimeSegmentID, **data)


class MSTS(XMLList):
	"""
	MSTS.xml
	"""
	
	def __init__(
			self,
			Version,
			IRMStatus=0,
			time_segments=None
			):
		"""

		:param Version:
		:type Version: int
		:param IRMStatus:
		:type IRMStatus: int
		:param time_segments:
		:type time_segments: List[TimeSegment]
		"""
		
		super().__init__(Version, time_segments)
		
		self.IRMStatus = int(IRMStatus)
		
	def to_dict(self):
		return dict(
				Version=self.Version,
				IRMStatus=self.IRMStatus,
				time_segments=list(self),
				)

	_content_type = TimeSegment
	_content_xml_name = "TimeSegment"

	@classmethod
	def from_xml(cls, element):
		class_ = super().from_xml(element)
		class_.IRMStatus = element.IRMStatus
		class_._append_from_element(element)
		
		return class_


def read_msts_xml(base_path):
	return MSTS.from_xml_file(base_path / "MSTS.xml")
