__all__ = [
		"PlatformError",
		"Unititialisable",
		"BDASpecData",
		"BDADataAccess",
		"IBDAChromData",
		"MSScanRecord",
		"BDAChromData",
		"BDAMSScanFileInformation",
		"BDAFileInformation",
		"SignalInfo",
		"ISignalInfo",
		"MassSpecDataReader",
		"IBDAFileInformation"
		]


class PlatformError(RuntimeError):
	"""
	Exception class to indicate that the current platform is unsupported.
	"""


class Unititialisable:
	"""
	Class to raise an error when trying to use the Agilent MHDAC on Linux/macOS.
	"""

	def __init__(self, *args, **kwargs):
		raise PlatformError("'pyms_agilent.mhdac' can only run on Windows.")


class BDASpecData(Unititialisable):  # noqa D101
	pass


class BDADataAccess(Unititialisable):  # noqa D101
	pass


class IBDAChromData(Unititialisable):  # noqa D101
	pass


class MSScanRecord(Unititialisable):  # noqa D101
	pass


class BDAChromData(Unititialisable):  # noqa D101
	pass


class BDAMSScanFileInformation(Unititialisable):  # noqa D101
	pass


class BDAFileInformation(Unititialisable):  # noqa D101
	pass


class SignalInfo(Unititialisable):  # noqa D101
	pass


class ISignalInfo(Unititialisable):  # noqa D101
	pass


class MassSpecDataReader(Unititialisable):  # noqa D101
	pass


class IBDAFileInformation(Unititialisable):  # noqa D101
	pass
