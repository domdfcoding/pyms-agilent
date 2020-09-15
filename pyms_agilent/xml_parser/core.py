#  !/usr/bin/env python
#
#  core.py
"""
Core functionality.
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import re
from abc import ABC
from typing import Any, Dict, Iterable, Optional, Type

# 3rd party
import lxml.objectify  # type: ignore
from attr_utils.docstrings import add_attrs_doc
from domdf_python_tools.bases import NamedList
from mh_utils.utils import camel_to_snake
from mh_utils.xml import XMLFileMixin

__all__ = ["make_from_element", "XMLList", "_get_from_enum", "tag2dict"]


def make_from_element(
		element: lxml.objectify.ObjectifiedElement,
		name: str,
		class_: Type,
		) -> Iterable:
	r"""
	Iterate over all child tags of ``element`` with the name ``name``
	and return an :class:`~collections.Iterable` containing instances of ``class_``
	constructed from the tags.

	:param element:
	:param name:
	:param class\_:
	"""  # noqa D400

	for item in element.findall(name):
		yield class_.from_xml(item)


@add_attrs_doc
class XMLList(XMLFileMixin, NamedList, ABC):
	"""
	Base class for lists generated from XML files.

	The list has an additional attribute :attr:`~pyms_agilent.xml_parser.core.XMLList.version`
	that indicates the version number of the XML file the data was generated from.

	:param version: The version number.
	:param initlist: Iterable to initialise the list from.
	"""

	def __init__(
			self,
			version: int,
			initlist: Optional[Iterable] = None,
			):
		super().__init__(initlist)
		self.version = int(version)

	#: The version number of the XML file the data in this list was generated from.
	version: int

	#: The type of object stored in the list.
	_content_type: Any = object

	#: The name of the XML element that members of this list should be constructed from.
	_content_xml_name = ''

	@classmethod
	def from_xml(cls, element: lxml.objectify.ObjectifiedElement) -> "XMLList":
		"""
		Construct a :class:`~.XMLList` object from an XML element.

		:param element: The XML element to parse the data from.
		"""

		return cls(element.Version)  # pragma: no cover

	def _append_from_element(self, element: lxml.objectify.ObjectifiedElement):
		"""
		Construct an object from an XML element and append it to this list.

		:param element:
		"""

		for item in make_from_element(element, self._content_xml_name, self._content_type):
			self.append(item)

		return self


def _get_from_enum(value: Any, enum, type_: Any = str) -> Any:
	r"""
	Returns the enum member representing the given value.

	:param value:
	:param enum:
	:type enum: :class:`enum.Enum`
	:param type\_:
	"""

	if isinstance(value, enum):
		return value
	else:
		return enum(type_(value))


def tag2dict(
		element: lxml.objectify.ObjectifiedElement,
		camel_lookup: Optional[Dict[str, str]] = None,
		xmlns: Optional[str] = None,
		) -> Dict[str, Any]:
	"""
	Returns a dictionary mapping child tags (converted from CamelCase to snake_case) to values.

	:param element: The element to parse tags from.
	:param camel_lookup: Optional mapping of CamelCase tag names to their snake_case equivalents.
	:param xmlns: Optional url that prefixes tag names, and which should be removed from the keys in the dictionary.
	"""

	output_dict: Dict[str, Any] = {}

	for tag in element.iterchildren():

		if xmlns:
			tag_name = re.sub(fr"^{{{xmlns}}}", '', tag.tag)
		else:
			tag_name = tag.tag

		if camel_lookup is not None:
			tag_name = camel_lookup.get(tag_name, camel_to_snake(tag_name))
		else:
			tag_name = camel_to_snake(tag_name)

		if isinstance(tag, lxml.objectify.IntElement):
			output_dict[tag_name] = int(tag.text)
		elif isinstance(tag, lxml.objectify.StringElement):
			output_dict[tag_name] = str(tag.text)
		elif isinstance(tag, lxml.objectify.FloatElement):
			output_dict[tag_name] = float(tag.text)
		else:
			output_dict[tag_name] = tag.text

	return output_dict
