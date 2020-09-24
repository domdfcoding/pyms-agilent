# stdlib
import sys

# 3rd party
import pytest

pytestmark = pytest.mark.skipif(condition=sys.platform != "win32", reason="Can only run these tests on Windows.")
