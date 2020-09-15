# stdlib
import datetime
import pathlib

# this package
from pyms_agilent.xml_parser.devices import Device, DeviceList, read_devices_xml


class TestDevice:

	def test_creation(self):
		device = Device(
				device_id=1011,
				display_name="HiP-ALS",
				model_number="G7167A",
				ordinal_number=1,
				serial_number="DEACK00183",
				type_=21,  # type: ignore
				stored_data_type=2,
				delay=0,
				vendor=1,
				)

		assert device.device_id == 1011
		assert device.display_name == "HiP-ALS"
		assert device.model_number == "G7167A"
		assert device.ordinal_number == 1
		assert device.serial_number == "DEACK00183"
		assert device.type_ == 21
		assert device.stored_data_type == 2
		assert device.delay == 0
		assert device.vendor == 1

		device = Device(device_id=1012)

		assert device.device_id == 1012
		assert device.display_name == ''
		assert device.model_number == ''
		assert device.ordinal_number == 0
		assert device.serial_number == ''
		assert device.type_ == 0
		assert device.stored_data_type == 0
		assert device.delay == 0
		assert device.vendor == 0

	def test_dict(self):

		device = Device(
				device_id=1011,
				display_name="HiP-ALS",
				model_number="G7167A",
				ordinal_number=1,
				serial_number="DEACK00183",
				type_=21,  # type: ignore
				stored_data_type=2,
				delay=0,
				vendor=1,
				)

		assert dict(device) == {
				"device_id": 1011,
				"display_name": "HiP-ALS",
				"driver_version": '',
				"firmware_version": '',
				"model_number": "G7167A",
				"ordinal_number": 1,
				"serial_number": "DEACK00183",
				"type_": 21,
				"stored_data_type": 2,
				"delay": 0,
				"vendor": 1,
				}


class TestDeviceList:

	def test_creation(self):
		assert DeviceList(version=1).version == 1
		assert DeviceList(version="1").version == 1  # type: ignore

		assert DeviceList(version=1, devices=[]) == []
		assert DeviceList(version=1, devices=()) == []

		device = Device(
				device_id=1011,
				display_name="HiP-ALS",
				model_number="G7167A",
				ordinal_number=1,
				serial_number="DEACK00183",
				type_=21,  # type: ignore
				stored_data_type=2,
				delay=0,
				vendor=1,
				)

		assert DeviceList(version=1, devices=[device]) == [device]

	def test_from_xml_file(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		device_list = DeviceList.from_xml_file(datafile / "AcqData" / "Devices.xml")
		assert isinstance(device_list, DeviceList)

		assert len(device_list) == 5
		assert device_list.version == 1

		assert isinstance(device_list[0], Device)
		assert device_list[0].device_id == 1
		assert device_list[0].display_name == "QTOF"
		assert device_list[0].driver_version == "8.00.00"
		assert device_list[0].firmware_version == "14.723"
		assert device_list[0].model_number == "G6550A"
		assert device_list[0].ordinal_number == 1
		assert device_list[0].serial_number == "SG1339B002"
		assert device_list[0].type_ == 6
		assert device_list[0].stored_data_type == 8
		assert device_list[0].delay == 0
		assert device_list[0].vendor == 1

	def test_read_devices_xml(self, monkeypatch):
		monkeypatch.chdir(pathlib.Path(__file__).parent)
		datafile = pathlib.Path("Propellant_Std_1ug_1_200124-0002.d")

		assert isinstance(read_devices_xml(datafile / "AcqData"), DeviceList)
