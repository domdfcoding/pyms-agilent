

class PlatformError(RuntimeError):
	pass


class Unititialisable:
	def __init__(self, *args, **kwargs):
		raise PlatformError("'pyms_agilent.mhdac' can only run on Windows.")


class BDASpecData(Unititialisable):
	pass


class BDADataAccess(Unititialisable):
	pass


class IBDAChromData(Unititialisable):
	pass


class MSScanRecord(Unititialisable):
	pass


class BDAChromData(Unititialisable):
	pass


class BDAMSScanFileInformation(Unititialisable):
	pass


class BDAFileInformation(Unititialisable):
	pass


class SignalInfo(Unititialisable):
	pass


class ISignalInfo(Unititialisable):
	pass


class MassSpecDataReader(Unititialisable):
	pass


class IBDAFileInformation(Unititialisable):
	pass
