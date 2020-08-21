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

# 3rd party
from enum_tools import IntEnum, StrEnum
from enum_tools.documentation import document_enum

__all__ = [
		"AcqStatusEnum",
		"MeasurementTypeEnum",
		"SeparationTechniqueEnum",
		"CalibrationTechniqueEnum",
		"CalibrationFormulaEnum",
		]


@document_enum
class AcqStatusEnum(IntEnum):
	"""
	Enumeration of values for the acquisition status.
	"""

	Init = 0  # doc: The acquisition has been initialised.
	Start = 1  # doc: The acquisition has started.
	End = 2  # doc: The acquisition has ended.


@document_enum
class MeasurementTypeEnum(IntEnum):
	"""
	Enumeration of values for the measurement type.
	"""

	Unknown = 0  # doc: Unknown measurement type.
	Infusion = 1  # doc: Infusion measurement type.
	Chromatographic = 2  # doc: Chromatographic measurement type.


@document_enum
class SeparationTechniqueEnum(IntEnum):
	"""
	Enumeration of values for the separation technique.
	"""

	Unspecified = 0  # doc: Unspecified separation technique.
	none = 1  # doc: No separation.
	GC = 2  # doc: Gas Chromatography separation technique.
	LC = 3  # doc: Liquid Chromatography separation technique.
	CE = 4  # doc: Capillary Electrophoresis separation technique.


@document_enum
class CalibrationTechniqueEnum(StrEnum):
	"""
	Enumeration of values for the calibration technique.
	"""

	ExternalReference = "ExternalReference"  # doc: External calibration reference.
	InternalReference = "InternalReference"  # doc: Internal calibration reference.
	Undefined = "Undefined"  # doc: Undefined calibration reference.


@document_enum
class CalibrationFormulaEnum(StrEnum):
	"""
	Enumeration of values for the calibration formula.
	"""

	Traditional = "Traditional"  # doc: Traditional calibration formula.
	Polynomial = "Polynomial"  # doc: Polynomial calibration formula.
	OriginalFourTerm = "OriginalFourTerm"  # doc: OriginalFourTerm calibration formula.
	Undefined = "Undefined"  # doc: Undefined calibration formula.
