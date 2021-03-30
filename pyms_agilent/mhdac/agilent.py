#  !/usr/bin/env python
#
#  agilent.py
"""
The lowest level interface to the Agilent MHDAC library.

This module handles registration of the Agilent ``.DLL`` files with Python.NET and exports the
``DataAnalysis`` module for use in the rest of ``pyms-agilent``.
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
import pathlib
import platform
import sys
from textwrap import dedent
from typing import TYPE_CHECKING

__all__ = ["DataAnalysis", "FileNotFoundException", "ArgumentOutOfRangeException", "NullReferenceException"]

if sys.platform == "win32" or TYPE_CHECKING:  # pragma: no cover (!Windows)
	# 3rd party
	import clr  # type: ignore

	if platform.architecture()[0] == "64bit":
		sys.path.append(str(pathlib.Path(__file__).parent / "x64"))
	else:
		sys.path.append(str(pathlib.Path(__file__).parent / "x86"))

	# 3rd party
	import System

	FileNotFoundException = System.IO.FileNotFoundException  # type: ignore  # TODO: update stubs
	ArgumentOutOfRangeException = System.ArgumentOutOfRangeException  # type: ignore  # TODO: update stubs
	NullReferenceException = System.NullReferenceException  # type: ignore  # TODO: update stubs

	try:
		clr.AddReference("MassSpecDataReader")
		clr.AddReference("BaseCommon")
		clr.AddReference("BaseDataAccess")
	except FileNotFoundException:
		raise FileNotFoundError(
				dedent(
						"""\
				Agilent MHDAC not found.

				Perhaps you need to install it with:

					$ python -m pyms_agilent.mhdac.install
				"""
						)
				)

	# 3rd party
	import Agilent
	import Agilent.MassSpectrometry.DataAnalysis

	DataAnalysis = Agilent.MassSpectrometry.DataAnalysis

else:  # pragma: no cover (Windows)

	# this package
	from pyms_agilent.mhdac import _posix_data_analysis

	DataAnalysis = _posix_data_analysis

	# These aren't public, so no docstrings needed


	class FileNotFoundException(IOError):  # noqa: D101
		pass

	class ArgumentOutOfRangeException(IndexError):  # noqa: D101
		pass

	class NullReferenceException(Exception):  # noqa: D101
		pass
