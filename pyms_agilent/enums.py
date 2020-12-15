#  !/usr/bin/env python
#
#  enums.py
"""
Enumerations.
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
from enum_tools import IntEnum, IntFlag, StrEnum
from enum_tools.documentation import document_enum

__all__ = [
		"AcqStatusEnum",
		"MeasurementTypeEnum",
		"SeparationTechniqueEnum",
		"CalibrationTechniqueEnum",
		"CalibrationFormulaEnum",
		"IRMStatus",
		"DeviceType",
		"DeviceVendor",
		"StoredDataType",
		"MSStorageMode",
		"MSScanType",
		"MSLevel",
		"IonizationMode",
		"ChromType",
		"DataUnit",
		"DataValueType",
		"FragmentationMode",
		"SpecType",
		"SampleCategory",
		"FragEnergyMode",
		"SpecSubType",
		"ChromSubType",
		"MeasurementType",
		"SeparationTechnique",
		"TofMsProcessingMode",
		"IonDetectorGain",
		"ImsFrameType",
		"ImsGateMode",
		"ImsMuxProcessing",
		"ImsTrapMode",
		"FragmentationClass",
		"FragmentationOpMode",  # "TofCalibrationFormula",
		# "FileType",
		"ApseBackgroundSource",
		"CompressionScheme",
		"IonPolarity",
		"DisplayPrecisionType",  # "ActualType",
		"DataFileValueDataType",  # "IonDetectorMode",
		"PointValueStorageScheme",
		"XSamplingType",
		"DesiredMSStorageType",
		"DisplayEffectType",  # "TofCalibrationTechnique"
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


@document_enum
class DeviceType(IntEnum):
	"""
	Enumeration of different detectors that can be used to obtain data.
	"""

	Unknown = 0  # doc: Unknown device.
	Mixed = 1  # doc: Mixed.
	Quadrupole = 2  # doc: Quadrupole Mass Spectrometer.
	IonTrap = 3  # doc: Ion Trap Mass Spectrometer.
	TimeOfFlight = 4  # doc: Time-of-Flight Mass Spectrometer.
	TandemQuadrupole = 5  # doc: Tandem Quadrupole Mass Spectrometer.
	QuadrupoleTimeOfFlight = 6  # doc: Quadrupole Time-of-Flight Mass Spectrometer.
	FlameIonizationDetector = 10  # doc: Flame Ionization Detector.
	ThermalConductivityDetector = 11  # doc: Thermal Conductivity Detector.
	RefractiveIndexDetector = 12  # doc: Refractive Index Detector.
	MultiWavelengthDetector = 13  # doc: Multi Wavelength Detector
	DiodeArrayDetector = 14  # doc: Diode Array Detector.
	VariableWavelengthDetector = 15  # doc: Variable Wavelength Detector.
	AnalogDigitalConverter = 16  # doc: Analog Digital Converter.
	ElectronCaptureDetector = 17  # doc: Electron Capture Detector.
	FluorescenceDetector = 18  # doc: Fluorescence Detector.
	EvaporativeLightScatteringDetector = 19  # doc: Evaporative Light Scattering Detector.
	ALS = 20  # doc: ALS.
	AutoSampler = 21  # Used to say WellPlateSampler  # doc: Autosampler.
	MicroWellPlateSampler = 22  # doc: Micro Well-plate Sampler.
	CTC = 23  # doc: CTC.
	IsocraticPump = 30  # doc: Isocratic Pump.
	BinaryPump = 31  # doc: Binary Pump.
	QuaternaryPump = 32  # doc: Quaternary Pump.
	CapillaryPump = 33  # doc: Capillary Pump.
	Nanopump = 34  # doc: Nano Pump.
	LowFlowPump = 35  # doc: Low Flow Pump.
	ThermostattedColumnCompartment = 40  # doc: Thermostatted Column Compartment.
	ChipCube = 41  # doc: Chip Cube.
	CANValves = 42  # doc: CAN Valves.
	UIB2 = 43  # doc: UIB 2.
	FlexCube = 44  # doc: Flex Cube.
	GCDetector = 50  # doc: GC Detector.  # Gas Chromatography?
	NitrogenPhosphorousDetector = 51  # doc: Nitrogen-Phosphorous Detector.
	FlamePhotometricDetector = 52  # doc: Flame Photomeric Detector.
	CE = 60  # doc: CE.
	SFC = 70  # doc: SFC.
	PumpValveCluster = 80  # doc: Pump Valve Cluster.
	ColumnCompCluster = 81  # doc: Column Comp Cluster.
	HDR = 82  # doc: HDR.
	MultiColumnCluster = 83  # doc: Multi-column Cluster.
	CompactLCIsoPump = 90  # doc: Compact Liquid Chromatography Isocratic Pump.
	CompactLCGradPump = 91  # doc: Compact Liquid Chromatography Gradient Pump.
	CompactLC1220IsoPump = 92  # doc: Compact Liquid Chromatography 1200-series Isocratic Pump.
	CompactLC1220GradPump = 93  # doc: Compact Liquid Chromatography 1200-series Gradient Pump.
	CompactLCColumnOven = 94  # doc: Compact Liquid Chromatography Column Oven.
	CompactLCSampler = 95  # doc: Compact Liquid Chromatography Autosampler.
	CompactLC1220Sampler = 96  # doc: Compact Liquid Chromatography 1200-series Autosampler.
	CompactLCVWD = 97  # doc: Compact Liquid Chromatography Variable Wavelength Detector.
	CompactLC1220VWD = 98  # doc: Compact Liquid Chromatography 1200-series Variable Wavelength Detector.
	CompactLC1220DAD = 99  # doc: Compact Liquid Chromatography 1200-series Diode Array Detector.


@document_enum
class DeviceVendor(IntEnum):
	"""
	Enumeration of values for device suppliers.
	"""

	Other = 0  # doc: The device was supplied by a company other than Agilent.
	Agilent = 1  # doc: The device was supplied by Agilent.


@document_enum
class StoredDataType(IntFlag):
	"""
	Enumeration of values for the type of stored data.
	"""

	Unspecified = 0  # doc: Unspecified data type.
	Chromatograms = 1  # doc: Chromatographic data.
	InstrumentCurves = 2  # doc: Instrument curve.
	Spectra = 4  # doc: Spectral data.
	MassSpectra = 8  # doc: Mass spectral data.
	All = 15  # doc: All data types.


@document_enum
class MSStorageMode(IntEnum):
	"""
	Enumeration of storage modes for Mass Spectrometry data.
	"""

	Unspecified = 0  # doc: Unspecified storage mode.
	Mixed = 1  # doc: Mixed storage modes.
	ProfileSpectrum = 2  # doc: Profile spectrum.
	PeakDetectedSpectrum = 3  # doc: Peak detected / centroid spectrum.


@document_enum
class MSScanType(IntFlag):
	"""
	Enumeration of values for the mass spectrometry scan type.
	"""

	Unspecified = 0  # doc: Unspecified scan type.
	Scan = 1  # doc: Scan
	SelectedIon = 2  # doc: Selected ion
	HighResolutionScan = 4  # doc: High resolution
	TotalIon = 8  # doc: Total ion
	AllMS = 15  # doc: All MS\ :superscript:`1` scan types.
	MultipleReaction = 256  # doc: Multiple reaction monitoring.
	ProductIon = 512  # doc: Product ion.
	PrecursorIon = 1024  # doc: Precursor ion.
	NeutralLoss = 2048  # doc: Neutral loss.
	NeutralGain = 4096  # doc: Neutral gain.
	AllMSN = 7936  # doc: All MS\ :superscript:`n` scan types.
	All = 7951  # doc: All scan types.


@document_enum
class MSLevel(IntEnum):
	"""
	Enumeration of the mass spectrometry level.
	"""

	All = 0  # doc: All MS levels.
	MS = 1  # doc: MS\ :superscript:`1`
	MSMS = 2  # doc: MS\ :superscript:`n`


@document_enum
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


@document_enum
class ChromType(IntEnum):
	"""
	Enumeration of different chromatogram types.
	"""

	Unspecified = 0  # doc: Unspecified chromatogram type.
	Signal = 1
	InstrumentParameter = 2  # doc: "Chromatogram" showing an instrument parameter.
	TotalWavelength = 3
	ExtractedWavelength = 4
	TotalIon = 5  # doc: A total ion chromatogram (TIC).
	BasePeak = 6  # doc: A base peak chromatogram (BPC)
	ExtractedIon = 7  # doc: An extracted ion chromatogram (EIC)
	ExtractedCompound = 8
	NeutralLoss = 9
	MultipleReactionMode = 10
	SelectedIonMonitoring = 11
	TotalCompound = 12
	AutoTotalIonBasePeak = 99


@document_enum
class DataUnit(IntEnum):
	"""
	Enumeration of different units used for data.
	"""

	Unspecified = 0  # doc: Unspecified unit.
	Mixed = 1  # doc: Mixed units.
	ScanNumber = 2  # doc: The scan number.
	Minutes = 3  # doc: Time in minutes.
	Seconds = 4  # doc: Time in seconds.
	Milliseconds = 5  # doc: Time in milliseconds.
	Microseconds = 6  # doc: Time in microseconds.
	Nanoseconds = 7  # doc: Time in nanoseconds.
	Nanometers = 8  # doc: Size/distance in nanometres (nm).
	Daltons = 9  # doc: Unit of atomic mass, named after the chemist :wikipedia:`John Dalton` (Da).
	Thomsons = 10  # doc: Unit of mass-to-charge ratio (Th).
	AbsorbanceUnits = 11
	Abundance = 12
	Volts = 13  # doc: Voltage
	Millivolts = 14
	Microvolts = 15
	Counts = 16
	MilliDaltons = 17  # doc: Millidaltons (mDa).
	PartsPerMillion = 18  # doc: Parts-per-million.
	AbsorptionUnits = 20
	AbundanceUnits = 21
	CountsPerSecond = 22  # doc: Number of counts per second.
	MilliAbsorbanceUnits = 26
	MilliThomsons = 28  # doc: Milli Thomsons (mTh)
	NoUnits = 30  # doc: No unit.
	Percent = 31  # doc: Percentage
	ResponseUnits = 32  # doc: Usually accompanied by a string giving the actual unit.
	Unit = 33
	UnitCharge = 34
	VoltageUnits = 35
	Centimeters = 36  # doc: Size/distance in centimetres (cm).
	Meters = 37  # doc: Size/distance in metres (m).


@document_enum
class DataValueType(IntEnum):
	"""
	Enumeration of values for the type of data.
	"""

	Unspecified = 0  # doc: Unspecified data type.
	Mixed = 1  # doc: Mixed data type.
	AcqTime = 2  # doc: Acquisition time.
	ScanNumber = 3  # doc: Scan number.
	Wavelength = 4
	MassToCharge = 5  # doc: Mass-to-charge ratio (|mz|).
	Mass = 6
	FlightTime = 7  # doc: Flight time.
	Response = 8
	OpticalEmission = 9  # doc: Optical emission.
	OpticalAbsorption = 10  # doc: Optical adsorption.
	RefractiveIndex = 11  # doc: Refractive index.
	Conductivity = 12
	Current = 13
	Voltage = 14
	IonAbundance = 15  # doc: Ion abundance.
	AccumulationTime = 19  # doc: Accumulation time.
	AcqTimeDifference = 20  # doc: Difference in acquisition time.
	AcqTimeResolution = 21  # doc: Resolution of the acquisition time.
	DoubleBondEquivalent = 22
	CorrelationCoefficient = 23  # doc: Correlation coefficient.
	DeconvolutedMass = 24  # doc: Deconvoluted mass.
	MassDifference = 25  # doc: Mass difference.
	MatchScore = 26  # doc: Match score.
	MaxMergeHeight = 27  # doc: Maximum merge height.
	MzDifference = 28  # doc: Difference in |mz|.
	MzResolution = 29  # doc: |mz| resolution.
	PeakArea = 30  # doc: Peak area.
	PeakAreaRatio = 31  # doc: Peak area ratio.
	Ordinate = 32
	PeakHeightRatio = 33  # doc: Peak height ratio.
	PeakSymmmetry = 34  # doc: Peak symmetry.
	PeakVolume = 35  # doc: Peak volume.
	PeakVolumeRatio = 36  # doc: Peak volume ratio.
	RelativeDifference = 38  # doc: Relative difference.
	SignalToNoise = 39  # doc: Signal-to-noise ratio.
	Analog = 40
	Pulse = 41
	AnalogToPulse = 42
	PulseToAnalogFactor = 43
	ImDriftTime = 44  # Ion mobility drift time.


@document_enum
class FragmentationMode(IntEnum):
	"""
	Enumeration of values for fragmentation modes.
	"""

	Unspecified = 0
	CID = 1
	ETD = 2


@document_enum
class SpecType(IntEnum):
	"""
	Enumeration of Spectrum types.

	.. _AMDIS: https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:amdis>
	"""

	Unspecified = 0  # doc: Unspecified spectrum type.
	UVSpectrum = 1  # doc: Ultraviolet spectrum.
	MassSpectrum = 2  # doc: Mass spectrum.
	TofMassSpectrum = 3  # doc: Time-of-flight mass spectrum.
	MassAndUVSpectra = 4  # doc: Mass and ultraviolet spectra.
	DeconvolutedMassSpectrum = 5  # doc: Deconvoluted mass spectrum.
	MFEMassSpectrum = 6
	AMDISDeconvSpectrum = 7  # doc: Mass spectrum deconvoluted by `AMDIS`_.
	FindByFormulaMassSpectrum = 8  # doc: Mass spectrum from MassHunter's "Find by Formula" search.
	LibraryMassSpectrum = 9  # doc: Library mass spectrum.
	AllIonsQualifiedIonMassSpectrum = 10


@document_enum
class SampleCategory(IntEnum):
	"""
	Enumeration of sample categories.
	"""

	Unspecified = 0
	General = 1
	OptimizationParams = 2
	CompoundParams = 4
	MassParams = 256
	CustomParams = 512
	UserParams = 1024
	All = 1799


@document_enum
class FragEnergyMode(IntEnum):
	"""
	Enumeration of fragmentation energy modes.
	"""

	Unspecified = 0
	Fixed = 1
	MultiSegment = 2


@document_enum
class SpecSubType(IntEnum):
	"""
	Enumeration of spectrum sub-types.
	"""

	Unspecified = 0
	HighE = 1
	LowE = 2


@document_enum
class ChromSubType(IntEnum):
	"""
	Enumeration of values for the chromatogram sub-type.
	"""

	Unspecified = 0  #: Unspecified sub-type.
	AllIonsFrag = 1
	ReferenceIon = 2


@document_enum
class MeasurementType(IntEnum):
	"""
	Enumeration of measurement types.
	"""

	Unknown = 0
	Infusion = 1
	Chromatographic = 2


@document_enum
class SeparationTechnique(IntEnum):
	"""
	Enumeration of separation techniques.
	"""

	Unspecified = 0  # doc: Unspecified separation technique.
	none = 1  # doc: No separation performed.
	GC = 2  # doc: Gas Chromatography.
	LC = 3  # doc: Liquid Chromatography.
	CE = 4  # doc: Capillary Electrophoresis/


@document_enum
class TofMsProcessingMode(IntEnum):
	"""
	Enumeration of processing modes for time-of-flight mass spectrometry.
	"""

	Unspecified = 0
	Raw = 1
	HiLow = 2
	DualGain = 4
	Tlpp = 8


@document_enum
class IonDetectorGain(IntEnum):
	"""
	Enumeration of ion detector gain modes.
	"""

	Unspecified = 0
	LowGain = 1
	HighGain = 2
	StitchedGain = 3
	Mixed = 999


@document_enum
class ImsFrameType(IntEnum):
	"""
	Enumeration of frame types for ion mobility spectrometry.
	"""

	Unspecified = 0
	Sample = 1
	Calibration = 2
	Prescan = 3
	Mixed = 999


@document_enum
class ImsGateMode(IntEnum):
	"""
	Enumeration of gate modes for ion mobility spectrometry.
	"""

	Unspecified = 0
	SingleGate = 1
	MuxGate = 2
	Mixed = 999


@document_enum
class ImsMuxProcessing(IntEnum):  # noqa: D101
	Unspecified = 0
	none = 1
	RealTime = 2
	PostRun = 3
	Mixed = 999


@document_enum
class ImsTrapMode(IntEnum):
	"""
	Enumeration of trap modes for ion mobility spectrometry.
	"""

	Unspecified = 0
	SingleTrap = 1
	DynamicTrap = 2
	MultiTrap = 3
	StitchedTrap = 4
	Mixed = 999


@document_enum
class FragmentationClass(IntEnum):
	"""
	Enumeration of values for the fragmentation class.
	"""

	Unspecified = 0
	LowEnergy = 1  # doc: Low energy fragmentation.
	HighEnergy = 2  # doc: High energy fragmentation.
	Mixed = 999


@document_enum
class FragmentationOpMode(IntEnum):  # noqa: D101
	Unspecified = 0
	none = 1
	Selective = 2
	NonSelective = 4
	HiLoFrag = 8


#
# @document_enum
# class TofCalibrationFormula(IntEnum):
# 	Unspecified = 0
# 	Mixed = 1
# 	Traditional = 2
# 	FourTerm = 3
# 	Polynomial = 4

#
# @document_enum
# class FileType(IntEnum):
# 	MSScanSchema = 256
# 	MSScanBinary = 257
# 	MSProfileBinary = 258
# 	MSPeakBinary = 259
# 	MSMassCalBinary = 260
# 	MSDefaultMassCal = 261
# 	MSTimeSegment = 262
# 	Contents = 263
# 	ScanActuals = 264
# 	PeriodicActuals = 265
# 	MethodParamChange = 272
# 	ChromDirectoryBinary = 512
# 	ChromatogramBinary = 513
# 	SpecDirectoryBinary = 514
# 	SpectrumBinary = 515
# 	MSUserCalBinary = 274
# 	MSUserCalIndexBinary = 273
# 	MSScan_XSpecific = 275
# 	ImsFrameBinary = 278
# 	ImsFrameMethod = 276
# 	ImsFrameSchema = 277


@document_enum
class ApseBackgroundSource(IntEnum):  # noqa: D101
	none = 0
	DesignatedBackgroundSpectrum = 1
	PeakStart = 2
	PeakEnd = 3
	PeakStartAndEnd = 4
	DesignatedTimeRange = 5


@document_enum
class CompressionScheme(IntEnum):
	"""
	Enumeration of values for the compression scheme.
	"""

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


@document_enum
class IonPolarity(IntEnum):  # noqa: D101
	Positive = 0
	Negative = 1
	Unassigned = 2
	Mixed = 3


@document_enum
class DisplayPrecisionType(IntEnum):  # noqa: D101
	DigitsAfterDecimal = 0
	Exponential = 1


# @document_enum
# class ActualType(IntEnum):
# 	Periodic = 0
# 	Scan = 1


@document_enum
class DataFileValueDataType(IntEnum):
	"""
	Enumeration of values for data types.
	"""

	Unspecified = 0
	Byte = 1
	Int16 = 2  # doc: 16 bit unsigned integer.
	Int32 = 3  # doc: 32 bit unsigned integer.
	Int64 = 4  # doc: 64 bit unsigned integer.
	Float32 = 5  # doc: 32 bit floating point number.
	Float64 = 6  # doc: 64 bit floating point number.


# @document_enum
# class IonDetectorMode(IntEnum):
# 	Unspecified = 0
# 	PulseCounting = 1
# 	Analog = 2
# 	Mixed = 3
# 	Error = 240


@document_enum
class PointValueStorageScheme(IntEnum):  # noqa: D101
	Unspecified = 0
	Mixed = 1
	Series = 2
	StartAndDelta = 3


@document_enum
class XSamplingType(IntEnum):  # noqa: D101
	Unspecified = 0
	Stepped = 1
	SparseStepped = 2
	Discontinuous = 4
	Irregular = 8
	Continuous = 16
	BoundedRegions = 32


@document_enum
class DesiredMSStorageType(IntEnum):
	"""
	Enumeration of values for the desired storage mode for the mass spectrometry data.
	"""

	Profile = 0
	Peak = 1
	ProfileElsePeak = 2
	PeakElseProfile = 3
	All = 4  # doc: All storage modes.
	Unspecified = 255  # doc: Unspecified storage mode.


@document_enum
class DisplayEffectType(IntEnum):  # noqa: D101
	Normal = 0
	Hidden = 1
	Bold = 2


# @document_enum
# class TofCalibrationTechnique(IntEnum):
# 	Unspecified = 0
# 	Mixed = 1
# 	ExternalReference = 2
# 	InternalReference = 3
