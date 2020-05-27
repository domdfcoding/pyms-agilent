#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  utils.py
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
import pathlib
import re
from distutils.util import strtobool


def as_path(val):
	val = str(val).strip()
	if val:
		return pathlib.PureWindowsPath(val)
	else:
		return None


def element_to_bool(element):
	element = str(element).strip()
	if element == "-1":
		return True
	else:
		return bool(strtobool(element))


def camel_to_snake(name):
	"""
	From https://stackoverflow.com/a/1176023/3092681
	"""
	name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
	return name.lower()

