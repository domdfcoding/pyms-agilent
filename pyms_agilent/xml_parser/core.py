#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  core.py
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
import pathlib
from abc import ABC, abstractmethod

# 3rd party
from domdf_python_tools.bases import namedlist
from lxml import etree, objectify


def get_data_from_element(data, element):
	for tag_name in list(data.keys()):
		tag = element.findall(tag_name)
		
		if tag:
			data[tag_name] = tag[0].text
	
	return data
	

def get_validated_tree(xml_file, schema_file=None):
	"""
	Returns a validated lxml objectify from the given XML file, validated against the schema file.
	
	:param xml_file:
	:type xml_file: str or pathlib.Path
	:param schema_file:
	:type schema_file: str or pathlib.Path or None
	
	:return:
	:rtype:
	"""
	
	schema = None
	if schema_file:
		schema = etree.XMLSchema(etree.parse(str(schema_file)))

	parser = objectify.makeparser(schema=schema)
	tree = objectify.parse(str(xml_file), parser=parser)
	
	if schema:
		assert schema.validate(tree)
	
	return tree


class VersionedList(namedlist()):
	"""
	List that also has a version number
	"""
	
	def __init__(
			self,
			Version,
			initlist=None,
			):
		"""

		:param Version:
		:type Version: int
		:param initlist:
		:type initlist:
		"""
		
		super().__init__(initlist)
		
		self.Version = int(Version)
	
	def to_dict(self):
		return dict(
				Version=self.Version,
				items=list(self),
				)
	
	@classmethod
	def from_xml(cls, element):
		Version = element.Version
		
		return cls(Version)


class XMLFileMixin(ABC):
	
	_schema = None
	
	@classmethod
	def from_xml_file(cls, filename):
		"""

		:param filename:
		:type filename: str or pathlib.Path

		:return:
		:rtype:
		"""
		
		tree = get_validated_tree(filename, cls._schema)
		root = tree.getroot()
		return cls.from_xml(root)

	@classmethod
	@abstractmethod
	def from_xml(cls, element):
		pass


def make_from_element(element, name, class_):
	for item in element.findall(name):
		yield class_.from_xml(item)


class XMLList(XMLFileMixin, VersionedList, ABC):
	
	_content_type = object
	_content_xml_name = ""
	
	def _append_from_element(self, element):
		
		for item in make_from_element(element, self._content_xml_name, self._content_type):
			self.append(item)
		
		return self


def _get_from_enum(value, enum, type_: any = str):
	if isinstance(value, enum):
		return value
	else:
		return enum(type_(value))
