#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  Contents.py
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

# 3rd party
import importlib_resources
from domdf_python_tools.bases import Dictable

# this package
from pyms_agilent.xml_parser import agilent_xsd
from .core import _get_from_enum, get_data_from_element, XMLFileMixin
from .enums import AcqStatusEnum, MeasurementTypeEnum, SeparationTechniqueEnum


class Contents(XMLFileMixin, Dictable):
	def __init__(
			self, Version=None, AcquiredTime=None, AcqStatus=None, InstrumentName='',
			LockedMode=None, MeasurementType=0, SeparationTechnique=0, TotalRunDuration=0.0,
			AcqSoftwareVersion=''):
		"""

		:param Version: The version number of something
		:type Version: int
		:param AcquiredTime: The acquisition time
		:type AcquiredTime: str or datetime.datetime
		:param AcqStatus:
		:type AcqStatus: AcqStatusEnum or int
		:param InstrumentName:
		:type InstrumentName: str
		:param LockedMode:
		:type LockedMode: bool
		:param MeasurementType:
		:type MeasurementType: MeasurementTypeEnum or int
		:param SeparationTechnique:
		:type SeparationTechnique: SeparationTechniqueEnum or int
		:param TotalRunDuration:
		:type TotalRunDuration: float or datetime.timedelta
		:param AcqSoftwareVersion:
		:type AcqSoftwareVersion: str
		"""
		
		super().__init__()
		
		self.Version = int(Version)
		
		if isinstance(AcquiredTime, datetime.datetime):
			self.AcquiredTime = AcquiredTime
		else:
			if ":" == AcquiredTime[-3]:
				AcquiredTime = AcquiredTime[:-3] + AcquiredTime[-2:]
			AcquiredTime = AcquiredTime[:19] + AcquiredTime[-5:]
			self.AcquiredTime = datetime.datetime.strptime(AcquiredTime, "%Y-%m-%dT%H:%M:%S%z")
		
		self.AcqStatus = _get_from_enum(AcqStatus, AcqStatusEnum, int)
		self.InstrumentName = str(InstrumentName)
		self.LockedMode = bool(LockedMode)
		self.MeasurementType = _get_from_enum(MeasurementType, MeasurementTypeEnum, int)
		self.SeparationTechnique = _get_from_enum(SeparationTechnique, SeparationTechniqueEnum, int)
		
		if isinstance(TotalRunDuration, datetime.timedelta):
			self.TotalRunDuration = TotalRunDuration
		else:
			self.TotalRunDuration = datetime.timedelta(seconds=float(TotalRunDuration))
		
		self.AcqSoftwareVersion = str(AcqSoftwareVersion)

	@property
	def __dict__(self):
		return dict(
				Version=self.Version,
				AcquiredTime=self.AcquiredTime,
				AcqStatus=int(self.AcqStatus),
				InstrumentName=self.InstrumentName,
				LockedMode=int(self.LockedMode),
				MeasurementType=int(self.MeasurementType),
				SeparationTechnique=int(self.SeparationTechnique),
				TotalRunDuration=self.TotalRunDuration,
				AcqSoftwareVersion=self.AcqSoftwareVersion,
				)

	with importlib_resources.path(agilent_xsd, "Contents.xsd") as schema_path:
		_schema = str(schema_path)
	
	@classmethod
	def from_xml(cls, element):
		
		data = {
				"Version": None, "AcquiredTime": None, "AcqStatus": None, "InstrumentName": '',
				"LockedMode": None, "MeasurementType": 0, "SeparationTechnique": 0,
				"TotalRunDuration": 0.0, "AcqSoftwareVersion": '',
				}
		
		data = get_data_from_element(data, element)
		
		return cls(**data)


def read_contents_xml(base_path):
	return Contents.from_xml_file(base_path / "Contents.xml")
