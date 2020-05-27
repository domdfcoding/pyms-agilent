#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  columns.py
"""
Properties for columns in a Worklist
"""
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
from collections import namedtuple
from typing import Any

# this package
from agilent_worklist_parser.enums import AttributeType
from agilent_worklist_parser.utils import as_path


def injection_volume(val):
	if val == -1:
		return "As Method"
	else:
		return int(val)


class Column(
		namedtuple('__BaseColumn', 'name, attribute_id, attribute_type, field_type, dtype, default_value, reorder_id')
		):
	"""

	Field Type - Each of the system defined columns have a field type starting from sampleid = 0 to reserved6 = 24
	Field Type - The system used column can be compound param = 35, optim param = 36, mass param = 37 and protein param = 38
	Field Type - The User added column  starts from 45

	:param name: The name of the column
	:type name: str
	:param attribute_id:
	:type attribute_id: int
	:param attribute_type: can be System Defined = 0, System Used = 1, User Added = 2
	:type attribute_type: AttributeType
	:param field_type:
	:type field_type: int
	:param dtype:
	:type dtype:
	:param default_value:
	:type default_value:
	:param reorder_id:
	:type reorder_id: int
	"""

	__slots__ = []

	def __new__(cls, name, attribute_id, attribute_type, dtype, default_value, field_type=None, reorder_id=None):
		name = str(name).strip()

		if dtype != Any:
			default_value = dtype(default_value)

		attribute_type = AttributeType(attribute_type)

		if not field_type:
			field_type = attribute_id
		if not reorder_id:
			reorder_id = attribute_id

		return super().__new__(
				cls, name, int(attribute_id), int(attribute_type), field_type, dtype, default_value, int(reorder_id)
				)

	def cast_value(self, value):
		if isinstance(value, str) and not value:
			return self.default_value

		if self.dtype == Any:
			return value
		else:
			return self.dtype(value)

	@classmethod
	def from_attribute(cls, attribute):

		if attribute.data_type == 8:
			dtype = str
		elif attribute.data_type == 5:
			dtype = float
		else:
			dtype = Any

		return Column(
				name=attribute.header_name,
				attribute_id=attribute.attribute_id,
				attribute_type=attribute.attribute_type,
				dtype=dtype,
				default_value=attribute.default_data_value,
				field_type=attribute.field_type,
				reorder_id=attribute.reorder_id,
				)


columns = {
		col.name: col
		for col in [
				Column(
						name="Sample ID",
						attribute_id=0,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						),
				Column(
						name="Sample Name",
						attribute_id=1,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						),
				Column(
						name="Rack Code",
						attribute_id=2,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						),
				Column(
						name="Rack Position",
						attribute_id=3,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						),
				Column(
						name="Plate Code",
						attribute_id=4,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						),
				Column(
						name="Plate Position",
						attribute_id=5,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						),
				Column(
						name="Sample Position",
						attribute_id=6,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						),
				Column(
						name="Method",
						attribute_id=7,
						attribute_type=AttributeType.SystemDefined,
						dtype=as_path,
						default_value=None,
						),
				Column(
						name="Override DA Method",
						attribute_id=8,
						attribute_type=AttributeType.SystemDefined,
						dtype=as_path,
						default_value=None,
						),
				Column(
						name="Data File",
						attribute_id=9,
						attribute_type=AttributeType.SystemDefined,
						dtype=as_path,
						default_value=None,
						),
				Column(
						name="Sample Type",
						attribute_id=10,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='Unknown',
						),
				Column(
						name="Method Type",
						attribute_id=11,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='Method No Override',
						reorder_id=12,
						),
				Column(
						name="Balance Override",
						attribute_id=12,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='No Override',
						reorder_id=13,
						),
				Column(
						name="Inj Vol (µl)",
						attribute_id=13,
						attribute_type=AttributeType.SystemDefined,
						dtype=injection_volume,
						default_value=5,
						reorder_id=14,
						),
				Column(
						name="Equilib Time (min)",
						attribute_id=14,
						attribute_type=AttributeType.SystemDefined,
						dtype=int,
						default_value=0,
						reorder_id=15,
						),
				Column(
						name="Dilution",
						attribute_id=15,
						attribute_type=AttributeType.SystemDefined,
						dtype=int,
						default_value=1,
						reorder_id=16,
						),
				Column(
						name="Wt/Vol",
						attribute_id=16,
						attribute_type=AttributeType.SystemDefined,
						dtype=float,
						default_value=0,
						reorder_id=17,
						),
				Column(
						name="Comment",
						attribute_id=17,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=18,
						),
				Column(
						name="Barcode",
						attribute_id=18,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=19,
						),
				Column(
						name="Reserved1",
						attribute_id=19,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=-1,
						),
				Column(
						name="Reserved2",
						attribute_id=20,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=-1,
						),
				Column(
						name="Reserved3",
						attribute_id=21,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=-1,
						),
				Column(
						name="Reserved4",
						attribute_id=22,
						attribute_type=AttributeType.SystemDefined,
						dtype=float,
						default_value=0,
						reorder_id=-1,
						),
				Column(
						name="Reserved5",
						attribute_id=23,
						attribute_type=AttributeType.SystemDefined,
						dtype=float,
						default_value=0,
						reorder_id=-1,
						),
				Column(
						name="Reserved6",
						attribute_id=24,
						attribute_type=AttributeType.SystemDefined,
						dtype=float,
						default_value=0,
						reorder_id=-1,
						),
				Column(
						name="Level Name",
						attribute_id=25,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=11,
						),
				Column(
						name="Sample Group",
						attribute_id=26,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=20,
						),
				Column(
						name="Info.",
						attribute_id=27,
						attribute_type=AttributeType.SystemDefined,
						dtype=str,
						default_value='',
						reorder_id=21,
						),
				]
		}
