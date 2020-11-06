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
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/pyms-agilent/latest?logo=read-the-docs
	:target: https://pyms-agilent.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/pyms-agilent/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/pyms-agilent/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/pyms-agilent/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/pyms-agilent
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/pyms-agilent/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/pyms-agilent/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/pyms-agilent/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/pyms-agilent/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/pyms-agilent/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/pyms-agilent/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/pyms-agilent/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/pyms-agilent?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/pyms-agilent?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/pyms-agilent
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

.. |license| image:: https://img.shields.io/github/license/domdfcoding/pyms-agilent
	:target: https://github.com/domdfcoding/pyms-agilent/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/pyms-agilent
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/pyms-agilent/v0.1.0
	:target: https://github.com/domdfcoding/pyms-agilent/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/pyms-agilent
	:target: https://github.com/domdfcoding/pyms-agilent/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/pyms-agilent/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/pyms-agilent/master
	:alt: pre-commit.ci status

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
