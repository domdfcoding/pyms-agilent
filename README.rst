================
pyms-agilent
================

.. start short_desc

**PyMassSpec interface to Agilent .d datafiles**

.. end short_desc

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/pyms-agilent/latest?logo=read-the-docs
	:target: https://pyms-agilent.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/PyMassSpec/pyms-agilent/workflows/Docs%20Check/badge.svg
	:target: https://github.com/PyMassSpec/pyms-agilent/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/PyMassSpec/pyms-agilent/workflows/Linux/badge.svg
	:target: https://github.com/PyMassSpec/pyms-agilent/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/PyMassSpec/pyms-agilent/workflows/Windows/badge.svg
	:target: https://github.com/PyMassSpec/pyms-agilent/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/PyMassSpec/pyms-agilent/workflows/macOS/badge.svg
	:target: https://github.com/PyMassSpec/pyms-agilent/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/PyMassSpec/pyms-agilent/workflows/Flake8/badge.svg
	:target: https://github.com/PyMassSpec/pyms-agilent/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/PyMassSpec/pyms-agilent/workflows/mypy/badge.svg
	:target: https://github.com/PyMassSpec/pyms-agilent/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/PyMassSpec/pyms-agilent/requirements.svg?branch=master
	:target: https://requires.io/github/PyMassSpec/pyms-agilent/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/PyMassSpec/pyms-agilent/master?logo=coveralls
	:target: https://coveralls.io/github/PyMassSpec/pyms-agilent?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/PyMassSpec/pyms-agilent?logo=codefactor
	:target: https://www.codefactor.io/repository/github/PyMassSpec/pyms-agilent
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/pyms-agilent
	:target: https://pypi.org/project/pyms-agilent/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pyms-agilent?logo=python&logoColor=white
	:target: https://pypi.org/project/pyms-agilent/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pyms-agilent
	:target: https://pypi.org/project/pyms-agilent/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/pyms-agilent
	:target: https://pypi.org/project/pyms-agilent/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/PyMassSpec/pyms-agilent
	:target: https://github.com/PyMassSpec/pyms-agilent/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/PyMassSpec/pyms-agilent
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/PyMassSpec/pyms-agilent/v0.1.2
	:target: https://github.com/PyMassSpec/pyms-agilent/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/PyMassSpec/pyms-agilent
	:target: https://github.com/PyMassSpec/pyms-agilent/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/pyms-agilent
	:target: https://pypi.org/project/pyms-agilent/
	:alt: PyPI - Downloads

.. end shields


Installation
--------------

.. start installation

``pyms-agilent`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install pyms-agilent

.. end installation

Additionally, the ``pyms_agilent.mhdac`` module requires the Agilent MassHunter Data Access Component to be installed.
This can be installed by running the following command and accepting the license:

.. code-block:: bash

	$ python -m pyms_agilent.mhdac.install
