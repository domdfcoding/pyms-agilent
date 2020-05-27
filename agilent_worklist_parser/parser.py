#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  parser.py
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
import datetime

from agilent_worklist_parser.columns import columns
from agilent_worklist_parser.tuples import Macro
# this package
from agilent_worklist_parser.utils import as_path, element_to_bool

sample_info_tags = {
		# Tag Name: Attribute
		"Identifier": 'Sample ID',
		"Name": 'Sample Name',
		"RackCode": 'Rack Code',
		"RackPosition": 'Rack Position',
		"PlateCode": 'Plate Code',
		"PlatePosition": 'Plate Position',
		"SamplePosition": 'Sample Position',
		"AcqMethod": 'Method',
		"DAMethod": 'Override DA Method',
		"DataFileName": 'Data File',
		"SampleType": 'Sample Type',
		"MethodExecutionType": 'Method Type',
		"BalanceType": 'Balance Override',
		"InjectionVolume": 'Inj Vol (µl)',
		"EquilibrationTime": 'Equilib Time (min)',
		"DilutionFactor": 'Dilution',
		"WeightPerVolume": 'Wt/Vol',
		"Description": 'Comment',
		"Barcode": 'Barcode',
		"Reserved1": 'Reserved1',
		"Reserved2": 'Reserved2',
		"Reserved3": 'Reserved3',
		"Reserved4": 'Reserved4',
		"Reserved5": 'Reserved5',
		"Reserved6": 'Reserved6',
		"CalibLevelName": 'Level Name',
		"SampleGroup": 'Sample Group',
		"SampleInformation": 'Info.',
		}


def parse_sample_info(element, user_columns):
	sample_info = {}

	acquired_time = str(element.AcqTime).strip()
	if acquired_time:
		if ":" == acquired_time[-3]:
			acquired_time = acquired_time[:-3] + acquired_time[-2:]
		acquired_time = acquired_time[:19] + acquired_time[-5:]
		sample_info["Acquired Time"] = datetime.datetime.strptime(acquired_time, "%Y-%m-%dT%H:%M:%S%z")
	else:
		sample_info["Acquired Time"] = datetime.datetime.fromtimestamp(0)

	sample_info["Sample Locked Run Mode"] = element_to_bool(element.SampleLockedRunMode)
	sample_info["Run Completed"] = element_to_bool(element.RunCompletedFlag)
	sample_info["Label"] = str(element.Label).strip()

	# SystemDefined attributes
	for tag_name, attr_name in sample_info_tags.items():
		column = columns[attr_name]

		sample_info[attr_name] = column.cast_value(str(getattr(element, tag_name)).strip())

	# SystemUsed and UserAdded attributes
	for tag in element.iterchildren("SampleDataArray"):
		for attr_name, column in user_columns.items():
			if column.attribute_id == int(tag.AttributeID):
				sample_info[attr_name] = column.cast_value(str(tag.DataValue).strip())

	return sample_info


def parse_params(element):
	params = dict(
			operator_name=str(element.OperatorName),
			# DataFileName=element.DataFileName,
			run_type=int(element.RunType),  # TODO: Enum, once values decoded
			method_execution_type=str(element.MethodExecutionType),
			acq_method_path=as_path(element.AcqMethodPath),
			da_method_path=as_path(element.DAMethodPath),
			export_output_path=as_path(element.ExportOutputPath),
			combine_export_output=element_to_bool(element.CombineExportOutput),
			combined_export_output_file=as_path(element.CombinedExportOutputFile),
			combine_output_by_plate=element_to_bool(element.CombineOutputByPlate),
			synchronous_execution=element_to_bool(element.SynchronousExecution),
			stop_worklist_on_da_error=element_to_bool(element.StopWorklistOnDAError),
			overlapped_injections=element_to_bool(element.OverlappedInjections),
			use_barcode=element_to_bool(element.UseBarcode),
			inject_on_barcode_mismatch=element_to_bool(element.InjectOnBarcodeMismatch),
			threshold_disk_space=int(element.ThresholdDiskSpace),
			ready_time_out=int(element.ReadyTimeOut),
			clear_run_checkbox=element_to_bool(element.ClearRunCheckBox),
			use_pre_worklist_macro=element_to_bool(element.UsePreWorklistMacro),
			pre_worklist_macro=Macro.from_xml(element.PreWorklistMacro),
			use_post_worklist_macro=element_to_bool(element.UsePostWorklistMacro),
			post_worklist_macro=Macro.from_xml(element.PostWorklistMacro),
			run_acq_clean_macro_on_error=element_to_bool(element.RunAcqCleanMacroOnError),
			acq_clean_macro=Macro.from_xml(element.AcqCleanMacro),
			use_post_analysis_macro=element_to_bool(element.UsePostAnalysisMacro),
			post_analysis_macro=Macro.from_xml(element.PostAnalysisMacro),
			description=str(element.Description).strip(),
			plate_bar_codes=element.PlateBarCodes,  # TODO: determine type
			)

	return params
