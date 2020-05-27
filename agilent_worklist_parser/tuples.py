#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  tuples.py
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

from agilent_worklist_parser.enums import AttributeType
# this package
from agilent_worklist_parser.utils import element_to_bool


class Checksum(namedtuple('__BaseChecksum', 'SchemaVersion, ALGO_VERSION, HASHCODE')):
	"""

	:param SchemaVersion:
	:type SchemaVersion: int
	:param ALGO_VERSION:
	:type ALGO_VERSION: int
	:param HASHCODE:
	:type HASHCODE: str
	"""

	__slots__ = []

	def __new__(cls, SchemaVersion, ALGO_VERSION, HASHCODE):
		return super().__new__(cls, int(SchemaVersion), int(ALGO_VERSION), str(HASHCODE))

	@classmethod
	def from_xml(cls, element):

		return cls(
				SchemaVersion=element.attrib["SchemaVersion"],
				ALGO_VERSION=element.attrib["ALGO_VERSION"],
				HASHCODE=element.MAIN.attrib["HASHCODE"]
				)


class Macro(namedtuple(
		'__BaseChecksum',
		'project_name, procedure_name, input_parameter, output_data_type, output_parameter, display_string'
		)):
	"""

	:param project_name:
	:type project_name: str
	:param procedure_name:
	:type procedure_name: str
	:param input_parameter:
	:type input_parameter: str
	:param output_data_type:
	:type output_data_type: int
	:param output_parameter:
	:type output_parameter: str
	:param display_string:
	:type display_string: str
	"""

	# TODO: enum for output_data_type

	__slots__ = []

	def __new__(cls, project_name, procedure_name, input_parameter, output_data_type, output_parameter, display_string):
		project_name = str(project_name).strip()
		procedure_name = str(procedure_name).strip()
		input_parameter = str(input_parameter).strip()
		output_parameter = str(output_parameter).strip()
		display_string = str(display_string).strip()

		return super().__new__(cls, project_name, procedure_name, input_parameter, int(output_data_type), output_parameter, display_string)

	@classmethod
	def from_xml(cls, element):

		return cls(
				project_name=element.ProjectName,
				procedure_name=element.ProcedureName,
				input_parameter=element.InputParameter,
				output_data_type=element.OutputDataType,
				output_parameter=element.OutputParameter,
				display_string=element.DisplayString,
				)

	@property
	def undefined(self):
		return all([
				self.project_name == '',
				self.procedure_name == '',
				self.input_parameter == '',
				self.output_data_type == 0,
				self.output_parameter == '',
				self.display_string == '',
				])

	def __repr__(self):
		if self.undefined:
			return f"{self.__class__.__name__}(Undefined)"
		else:
			return super().__repr__()


class Attribute(namedtuple(
		'__BaseAttribute',
		'attribute_id, attribute_type, field_type, system_name, header_name, data_type, '
		'default_data_value, reorder_id, show_hide_status, column_width'
		)):
	"""

	Field Type - Each of the system defined columns have a field type starting from sampleid = 0 to reserved6 = 24
	Field Type - The system used column can be compound param = 35, optim param = 36, mass param = 37 and protein param = 38
	Field Type - The User added column  starts from 45

	:param attribute_id:
	:type attribute_id: int
	:param attribute_type: can be System Defined = 0, System Used = 1, User Added = 2
	:type attribute_type: AttributeType
	:param field_type:
	:type field_type: int
	:param system_name:
	:type system_name: str
	:param header_name:
	:type header_name: str
	:param data_type:
	:type data_type:
	:param default_data_value:
	:type default_data_value:
	:param reorder_id:
	:type reorder_id: int
	:param show_hide_status:
	:type show_hide_status: bool
	:param column_width:
	:type column_width: int
	"""

	# TODO: enum for output_data_type

	__slots__ = []

	def __new__(
			cls, attribute_id, attribute_type, field_type, system_name, header_name,
			data_type, default_data_value, reorder_id, show_hide_status, column_width):
		system_name = str(system_name).strip()
		header_name = str(header_name).strip()
		default_data_value = str(default_data_value).strip()
		# TODO: determine data_type and use it to cast the values and the default value
		"""
		Perhaps
DataFileValuedata_type = bdict(
	Unspecified=0,
	Byte=1,
	Int16=2,
	Int32=3,
	Int64=4,
	Float32=5,
	Float64=6,
)
		"""

		return super().__new__(
				cls, int(attribute_id), AttributeType(attribute_type), int(field_type),
				system_name, header_name, int(data_type), default_data_value,
				int(reorder_id), element_to_bool(show_hide_status), int(column_width))

	@classmethod
	def from_xml(cls, element):

		return cls(
				attribute_id=element.AttributeID,
				attribute_type=element.AttributeType,
				field_type=element.FieldType,
				system_name=element.SystemName,
				header_name=element.HeaderName,
				data_type=element.DataType,
				default_data_value=element.DefaultDataValue,
				reorder_id=element.ReorderID,
				show_hide_status=element.ShowHideStatus,
				column_width=element.ColumnWidth,
				)
