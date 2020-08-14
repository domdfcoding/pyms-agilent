#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  enums.py
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
from enum import Enum

# 3rd party
from enum_tools import IntEnum, StrEnum


class AcqStatusEnum(IntEnum):
	Init = 0
	Start = 1
	End = 2


class MeasurementTypeEnum(IntEnum):
	Unknown = 0
	Infusion = 1
	Chromatographic = 2


class SeparationTechniqueEnum(IntEnum):
	Unspecified = 0
	none = 1
	GC = 2
	LC = 3
	CE = 4


class CalibrationTechniqueEnum(StrEnum):
	ExternalReference = "ExternalReference"
	InternalReference = "InternalReference"
	Undefined = "Undefined"


class CalibrationFormulaEnum(StrEnum):
	Traditional = "Traditional"
	Polynomial = "Polynomial"
	OriginalFourTerm = "OriginalFourTerm"
	Undefined = "Undefined"
