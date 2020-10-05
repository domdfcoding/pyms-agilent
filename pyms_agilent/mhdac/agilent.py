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
from typing import TYPE_CHECKING

__all__ = ["DataAnalysis", "FileNotFoundException", "ArgumentOutOfRangeException", "NullReferenceException"]

if sys.platform == "win32" or TYPE_CHECKING:
	# 3rd party
	import clr  # type: ignore

	if platform.architecture()[0] == "64bit":
		sys.path.append(str(pathlib.Path(__file__).parent / "x64"))
	else:
		sys.path.append(str(pathlib.Path(__file__).parent / "x86"))

	clr.AddReference("MassSpecDataReader")
	clr.AddReference("BaseCommon")
	clr.AddReference("BaseDataAccess")

	# 3rd party
	import Agilent
	import Agilent.MassSpectrometry.DataAnalysis
	import System

	DataAnalysis = Agilent.MassSpectrometry.DataAnalysis

	FileNotFoundException = System.IO.FileNotFoundException
	ArgumentOutOfRangeException = System.ArgumentOutOfRangeException
	NullReferenceException = System.NullReferenceException

else:
	# this package
	from pyms_agilent.mhdac import _posix_data_analysis
	DataAnalysis = _posix_data_analysis

	class FileNotFoundException(IOError):
		pass

	class ArgumentOutOfRangeException(IndexError):
		pass

	class NullReferenceException(Exception):
		pass
