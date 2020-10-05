# 3rd party
import pytest

# this package
from pyms_agilent.exceptions import PlatformError, Unititialisable


def test_unititialisable():

	with pytest.raises(PlatformError, match="'pyms_agilent.mhdac' can only run on Windows."):
		Unititialisable()

	class Subclass(Unititialisable):
		pass

	with pytest.raises(PlatformError, match="'pyms_agilent.mhdac' can only run on Windows."):
		Subclass()

	class Subclass2(Unititialisable):

		def __init__(self, *args, **kwargs):
			pass

	with pytest.raises(PlatformError, match="'pyms_agilent.mhdac' can only run on Windows."):
		Subclass2()
