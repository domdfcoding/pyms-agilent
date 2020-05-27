#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  classes.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from collections.abc import Sequence
from pprint import pformat

# 3rd party
import pandas
from domdf_python_tools.bases import Dictable

# this package
from agilent_worklist_parser.columns import Column, columns
from agilent_worklist_parser.enums import AttributeType
from agilent_worklist_parser.parser import parse_params, parse_sample_info
from agilent_worklist_parser.tuples import Attribute, Checksum
from pyms_agilent.xml_parser.core import XMLFileMixin


class JobData(Dictable):

	def __init__(self, id: str, job_type: int, run_status: int, sample_info: dict = None):
		"""

		:param id:
		:type id:
		:param job_type:
		:type job_type:
		:param run_status:
		:type run_status:
		:param sample_info:
		:type sample_info:
		"""

		super().__init__()

		self.id = str(id)
		self.job_type = int(job_type)
		self.run_status = int(run_status)

		if sample_info:
			self.sample_info = sample_info
		else:
			self.sample_info = {}

	__slots__ = ["id", "job_type", "run_status", "sample_info"]

	# dtypes
	# 8: Str
	# Inj Vol, Dilution and Equilib Time (min) 5

	@classmethod
	def from_xml(cls, element, user_columns):

		return cls(
				id=element.ID,
				job_type=element.JobType,
				run_status=element.RunStatus,
				sample_info=parse_sample_info(element.SampleInfo, user_columns),
				)

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	def __repr__(self):
		values = ', '.join(f'{key}={val!r}' for key, val in iter(self) if key != 'sample_info')
		return f"{self.__class__.__name__}({values})"


class Worklist(XMLFileMixin, Dictable):

	def __init__(self, version, locked_run_mode, instrument_name, params, user_columns, jobs, checksum):
		"""

		:param version:
		:type version: float
		:param locked_run_mode:
		:type locked_run_mode: bool
		:param instrument_name:
		:type instrument_name: str
		:param params:
		:type params: dict
		:param user_columns:
		:type user_columns: dict
		:param jobs:
		:type jobs: Sequence[JobData]
		:param checksum:
		:type checksum: Checksum
		"""

		super().__init__()

		self.version = version
		self.locked_run_mode = bool(locked_run_mode)
		self.instrument_name = str(instrument_name)
		self.params = params
		self.user_columns = user_columns
		self.jobs = list(jobs)
		self.checksum = checksum

	__slots__ = ["version", "user_columns", "jobs", "checksum", "locked_run_mode", "instrument_name", "params"]

	@property
	def __dict__(self):
		data = {}
		for key in self.__slots__:
			data[key] = getattr(self, key)

		return data

	@classmethod
	def from_xml(cls, element):

		version = float(element.Version)
		checksum = Checksum.from_xml(element.Checksum)

		WorklistInfo = element.WorklistInfo

		if WorklistInfo.LockedRunMode == -1:
			locked_run_mode = True
		elif WorklistInfo.LockedRunMode == 0:
			locked_run_mode = False
		else:
			raise ValueError("Unknown value for 'LockedRunMode'")

		instrument_name = str(WorklistInfo.Instrument)
		params = parse_params(WorklistInfo.Params)

		attributes_list = []
		jobs_list = []

		user_columns = {}

		for attribute in WorklistInfo.AttributeInformation.iterchildren("Attributes"):
			attribute = Attribute.from_xml(attribute)
			attributes_list.append(attribute)

			if attribute.attribute_type != AttributeType.SystemDefined:
				column = Column.from_attribute(attribute)
				user_columns[column.name] = column

		for job in WorklistInfo.JobDataList.iterchildren("JobData"):
			jobs_list.append(JobData.from_xml(job, user_columns))

		return cls(
				version=version,
				locked_run_mode=locked_run_mode,
				instrument_name=instrument_name,
				params=params,
				user_columns=user_columns,
				jobs=jobs_list,
				checksum=checksum,
				)

	def __repr__(self):
		return f"{self.__class__.__name__}({pformat(dict(self))})"

	def as_dataframe(self):
		headers = [col for col in columns] + [col for col in self.user_columns]
		data = []

		for job in self.jobs:
			row = []

			for header_label in headers:
				row.append(job.sample_info[header_label])

			data.append(row)

		# TODO: Sort columns by "reorder_id"

		return pandas.DataFrame(data, columns=headers)
