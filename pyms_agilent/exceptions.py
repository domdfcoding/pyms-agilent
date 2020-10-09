#  !/usr/bin/env python
#
#  exceptions.py
"""
Exception classes.
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

__all__ = ["NotMS2Error", "PlatformError", "Unititialisable"]


class NotMS2Error(ValueError):
	r"""
	Raised when trying to access MS\ :superscript:`2` attributes
	for data that was acquired in MS\ :superscript:`1` mode.
	"""  # noqa D400


class PlatformError(RuntimeError):
	"""
	Exception class to indicate that the current platform is unsupported.
	"""


class Unititialisable:
	"""
	Class to raise an error when trying to use the Agilent MHDAC on Linux/macOS.

	:raises PlatformError: on initialisation.
	"""

	def __init__(self, *args, **kwargs):
		raise PlatformError("'pyms_agilent.mhdac' can only run on Windows.")

	def __init_subclass__(cls, **kwargs):
		if cls.__init__ is not Unititialisable.__init__:
			cls.__init__ = Unititialisable.__init__  # type: ignore
