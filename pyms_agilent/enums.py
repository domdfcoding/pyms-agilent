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
#  Parts of this file based on multiplierz
#  https://github.com/BlaisProteomics/multiplierz
#  © Blais Proteomics Center, Dana-Farber Cancer Institute
#  Licensed under the GNU Lesser General Public License v3
#  See also: Alexander, William M., et al. "multiplierz v2.0:
#    a Python‐based ecosystem for shared access and analysis of
#    native mass spectrometry data." Proteomics (2017).
#
#  Parts of this file based on ms_deisotope
#  https://github.com/mobiusklein/ms_deisotope
#  © Joshua Klein (mobiusklein), Boston University Medical Campus
#  Licensed under the Apache License 2.0
#

# 3rd party
from enum import IntFlag

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
	Stop = 3  # doc: The acquisition has stopped.


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


@document_enum
class IRMStatus(IntFlag):
	"""
	Enumeration of possible values for the IRM/Runtime calibration status.
	"""

	Success = 0  # doc: Success
	SomeIonsMissed = 1  # doc: Some ions were missed
	AllIonsMissed = 2  # doc: All ions were missed


class DeviceType(IntEnum):
	"""
	Enumeration of different detectors that can be used to obtain data.
	"""

	Unknown = 0
	Mixed = 1
	Quadrupole = 2
	IonTrap = 3
	TimeOfFlight = 4
	TandemQuadrupole = 5
	QuadrupoleTimeOfFlight = 6
	FlameIonizationDetector = 10
	ThermalConductivityDetector = 11
	RefractiveIndexDetector = 12
	MultiWavelengthDetector = 13
	DiodeArrayDetector = 14
	VariableWavelengthDetector = 15
	AnalogDigitalConverter = 16
	ElectronCaptureDetector = 17
	FluorescenceDetector = 18
	EvaporativeLightScatteringDetector = 19
	ALS = 20
	AutoSampler = 21  # Used to say WellPlateSampler
	MicroWellPlateSampler = 22
	CTC = 23
	IsocraticPump = 30
	BinaryPump = 31
	QuaternaryPump = 32
	CapillaryPump = 33
	Nanopump = 34
	LowFlowPump = 35
	ThermostattedColumnCompartment = 40
	ChipCube = 41
	CANValves = 42
	UIB2 = 43
	FlexCube = 44
	GCDetector = 50
	NitrogenPhosphorousDetector = 51
	FlamePhotometricDetector = 52
	CE = 60
	SFC = 70
	PumpValveCluster = 80
	ColumnCompCluster = 81
	HDR = 82
	MultiColumnCluster = 83
	CompactLCIsoPump = 90
	CompactLCGradPump = 91
	CompactLC1220IsoPump = 92
	CompactLC1220GradPump = 93
	CompactLCColumnOven = 94
	CompactLCSampler = 95
	CompactLC1220Sampler = 96
	CompactLCVWD = 97
	CompactLC1220VWD = 98
	CompactLC1220DAD = 99


@document_enum
class DeviceVendor(IntEnum):
	"""
	Enumeration of values for device suppliers.
	"""

	Other = 0  # doc: The device was supplied by a company other than Agilent.
	Agilent = 1  # doc: The device was supplied by Agilent.


class StoredDataType(IntFlag):
	"""
	Enumeration of values for the type of stored data.
	"""

	Unspecified = 0
	Chromatograms = 1
	InstrumentCurves = 2
	Spectra = 4
	MassSpectra = 8
	All = 15


class MSStorageMode(IntEnum):
	"""
	Enumeration of storage modes for Mass Spectrometry data.
	"""

	Unspecified = 0
	Mixed = 1
	ProfileSpectrum = 2
	PeakDetectedSpectrum = 3  # Centroid


class MSScanType(IntFlag):
	"""
	Enumeration of values for the mass spectrometry scan type.
	"""

	Unspecified = 0
	Scan = 1
	SelectedIon = 2
	HighResolutionScan = 4
	TotalIon = 8
	AllMS = 15
	MultipleReaction = 256
	ProductIon = 512
	PrecursorIon = 1024
	NeutralLoss = 2048
	NeutralGain = 4096
	AllMSN = 7936
	All = 7951


class MSLevel(IntEnum):
	"""
	Enumeration of the mass spectrometry level.
	"""

	All = 0
	MS = 1
	MSMS = 2


class IonizationMode(IntFlag):
	"""
	Enumeration of different mass spectrometry ionization modes.
	"""

	Unspecified = 0
	Mixed = 1
	EI = 2
	CI = 4
	Maldi = 8
	Appi = 16
	Apci = 32
	ESI = 64
	NanoEsi = 128
	MsChip = 512
	ICP = 1024
	Jetstream = 2048


class ChromType(IntEnum):
	"""
	Enumeration of different chromatogram types.
	"""

	Unspecified = 0
	Signal = 1
	InstrumentParameter = 2
	TotalWavelength = 3
	ExtractedWavelength = 4
	TotalIon = 5
	BasePeak = 6
	ExtractedIon = 7
	ExtractedCompound = 8
	NeutralLoss = 9
	MultipleReactionMode = 10
	SelectedIonMonitoring = 11
	TotalCompound = 12
	AutoTotalIonBasePeak = 99


class DataUnit(IntEnum):
	"""
	Enumeration of different units used for data.
	"""

	Unspecified = 0
	Mixed = 1
	ScanNumber = 2
	Minutes = 3
	Seconds = 4
	Milliseconds = 5
	Microseconds = 6
	Nanoseconds = 7
	Nanometers = 8
	Daltons = 9
	Thomsons = 10
	AbsorbanceUnits = 11
	Abundance = 12
	Volts = 13
	Millivolts = 14
	Microvolts = 15
	Counts = 16
	MilliDaltons = 17
	PartsPerMillion = 18
	AbsorptionUnits = 20
	AbundanceUnits = 21
	CountsPerSecond = 22
	MilliAbsorbanceUnits = 26
	MilliThomsons = 28
	NoUnits = 30
	Percent = 31
	ResponseUnits = 32
	Unit = 33
	UnitCharge = 34
	VoltageUnits = 35
	Centimeters = 36
	Meters = 37


class DataValueType(IntEnum):
	"""
	Enumeration of values for the type of data.
	"""

	Unspecified = 0
	Mixed = 1
	AcqTime = 2
	ScanNumber = 3
	Wavelength = 4
	MassToCharge = 5
	Mass = 6
	FlightTime = 7
	Response = 8
	OpticalEmission = 9
	OpticalAbsorption = 10
	RefractiveIndex = 11
	Conductivity = 12
	Current = 13
	Voltage = 14
	IonAbundance = 15
	AccumulationTime = 19
	AcqTimeDifference = 20
	AcqTimeResolution = 21
	DoubleBondEquivalent = 22
	CorrelationCoefficient = 23
	DeconvolutedMass = 24
	MassDifference = 25
	MatchScore = 26
	MaxMergeHeight = 27
	MzDifference = 28
	MzResolution = 29
	PeakArea = 30
	PeakAreaRatio = 31
	Ordinate = 32
	PeakHeightRatio = 33
	PeakSymmmetry = 34
	PeakVolume = 35
	PeakVolumeRatio = 36
	RelativeDifference = 38
	SignalToNoise = 39
	Analog = 40
	Pulse = 41
	AnalogToPulse = 42
	PulseToAnalogFactor = 43
	ImDriftTime = 44


class FragmentationMode(IntEnum):
	Unspecified = 0
	CID = 1
	ETD = 2


class SpecType(IntEnum):
	"""
	Enumeration of Spectrum types.
	"""

	Unspecified = 0
	UVSpectrum = 1
	MassSpectrum = 2
	TofMassSpectrum = 3
	MassAndUVSpectra = 4
	DeconvolutedMassSpectrum = 5
	MFEMassSpectrum = 6
	AMDISDeconvSpectrum = 7
	FindByFormulaMassSpectrum = 8
	LibraryMassSpectrum = 9
	AllIonsQualifiedIonMassSpectrum = 10


class SampleCategory(IntEnum):
	Unspecified = 0
	General = 1
	OptimizationParams = 2
	CompoundParams = 4
	MassParams = 256
	CustomParams = 512
	UserParams = 1024
	All = 1799


class FragEnergyMode(IntEnum):
	Unspecified = 0
	Fixed = 1
	MultiSegment = 2


class SpecSubType(IntEnum):
	Unspecified = 0
	HighE = 1
	LowE = 2


class ChromSubType(IntEnum):
	Unspecified = 0
	AllIonsFrag = 1
	ReferenceIon = 2


class MeasurementType(IntEnum):
	Unknown = 0
	Infusion = 1
	Chromatographic = 2


class SeparationTechnique(IntEnum):
	"""
	Enumeration of separation techniques.
	"""
	Unspecified = 0
	none = 1
	GC = 2
	LC = 3
	CE = 4


class TofMsProcessingMode(IntEnum):
	Unspecified = 0
	Raw = 1
	HiLow = 2
	DualGain = 4
	Tlpp = 8


class IonDetectorGain(IntEnum):
	Unspecified = 0
	LowGain = 1
	HighGain = 2
	StitchedGain = 3
	Mixed = 999


class ImsFrameType(IntEnum):
	Unspecified = 0
	Sample = 1
	Calibration = 2
	Prescan = 3
	Mixed = 999


class ImsGateMode(IntEnum):
	Unspecified = 0
	SingleGate = 1
	MuxGate = 2
	Mixed = 999


class ImsMuxProcessing(IntEnum):
	Unspecified = 0
	_None = 1
	RealTime = 2
	PostRun = 3
	Mixed = 999


class ImsTrapMode(IntEnum):
	Unspecified = 0
	SingleTrap = 1
	DynamicTrap = 2
	MultiTrap = 3
	StitchedTrap = 4
	Mixed = 999


class FragmentationClass(IntEnum):
	Unspecified = 0
	LowEnergy = 1
	HighEnergy = 2
	Mixed = 999


class FragmentationOpMode(IntEnum):
	Unspecified = 0
	_None = 1
	Selective = 2
	NonSelective = 4
	HiLoFrag = 8


class TofCalibrationFormula(IntEnum):
	Unspecified = 0
	Mixed = 1
	Traditional = 2
	FourTerm = 3
	Polynomial = 4


class FileType(IntEnum):
	MSScanSchema = 256
	MSScanBinary = 257
	MSProfileBinary = 258
	MSPeakBinary = 259
	MSMassCalBinary = 260
	MSDefaultMassCal = 261
	MSTimeSegment = 262
	Contents = 263
	ScanActuals = 264
	PeriodicActuals = 265
	MethodParamChange = 272
	ChromDirectoryBinary = 512
	ChromatogramBinary = 513
	SpecDirectoryBinary = 514
	SpectrumBinary = 515
	MSUserCalBinary = 274
	MSUserCalIndexBinary = 273
	MSScan_XSpecific = 275
	ImsFrameBinary = 278
	ImsFrameMethod = 276
	ImsFrameSchema = 277


class ApseBackgroundSource(IntEnum):
	none = 0
	DesignatedBackgroundSpectrum = 1
	PeakStart = 2
	PeakEnd = 3
	PeakStartAndEnd = 4
	DesignatedTimeRange = 5


class CompressionScheme(IntEnum):
	none = 0
	DataRange = 1
	Threshold = 2
	Wiff = 4
	PackedFloat = 8
	LPC = 16
	TOF_NONE = 32
	OneDataRange = 64
	DeflateStream = 128
	GZipStream = 256
	LZF = 512
	RlzPlain = 1024
	RlzInt = 2048
	RlzByte = 4096


class IonPolarity(IntEnum):
	Positive = 0
	Negative = 1
	Unassigned = 2
	Mixed = 3


class DisplayPrecisionType(IntEnum):
	DigitsAfterDecimal = 0
	Exponential = 1


class ActualType(IntEnum):
	Periodic = 0
	Scan = 1


class DataFileValueDataType(IntEnum):
	Unspecified = 0
	Int16 = 2
	Int32 = 3
	Int64 = 4
	Float32 = 5
	Float64 = 6
	Byte = 1


class IonDetectorMode(IntEnum):
	Unspecified = 0
	PulseCounting = 1
	Analog = 2
	Mixed = 3
	Error = 240


class PointValueStorageScheme(IntEnum):
	Unspecified = 0
	Mixed = 1
	Series = 2
	StartAndDelta = 3


class XSamplingType(IntEnum):
	Unspecified = 0
	Stepped = 1
	SparseStepped = 2
	Discontinuous = 4
	Irregular = 8
	Continuous = 16
	BoundedRegions = 32


class DesiredMSStorageType(IntEnum):
	Profile = 0
	Peak = 1
	ProfileElsePeak = 2
	PeakElseProfile = 3
	All = 4
	Unspecified = 255


class DisplayEffectType(IntEnum):
	Normal = 0
	Hidden = 1
	Bold = 2


class TofCalibrationTechnique(IntEnum):
	Unspecified = 0
	Mixed = 1
	ExternalReference = 2
	InternalReference = 3
