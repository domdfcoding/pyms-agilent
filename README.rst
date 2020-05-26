****************
pyms-agilent
****************

.. start shields 

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs|
	* - Tests
	  - |travis| |requires| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Other
	  - |license| |language| |commits-since| |commits-latest| |maintained| 
	
.. |docs| image:: https://readthedocs.org/projects/pyms-agilent/badge/?version=latest
	:target: https://pyms-agilent.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/pyms-agilent/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/pyms-agilent
	:alt: Travis Build Status
	
.. |requires| image:: https://requires.io/github/domdfcoding/pyms-agilent/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/pyms-agilent/requirements/?branch=master
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/pyms-agilent
	:target: https://www.codefactor.io/repository/github/domdfcoding/pyms-agilent
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/pyms-agilent.svg
	:target: https://pypi.org/project/pyms-agilent/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pyms-agilent.svg
	:target: https://pypi.org/project/pyms-agilent/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pyms-agilent
	:target: https://pypi.org/project/pyms-agilent/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/pyms-agilent
	:target: https://pypi.org/project/pyms-agilent/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/pyms-agilent
	:alt: License
	:target: https://github.com/domdfcoding/pyms-agilent/blob/master/LICENSE

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/pyms-agilent
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/pyms-agilent/v0.0.1
	:target: https://github.com/domdfcoding/pyms-agilent/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/pyms-agilent
	:target: https://github.com/domdfcoding/pyms-agilent/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. end shields

PyMassSpec interface to Agilent .d datafiles

|

Installation
--------------

``pyms-agilent`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

    $ python -m pip install pyms-agilent

To install with ``conda``:

.. code-block:: bash

    $ conda config --add channels http://conda.anaconda.org/domdfcoding
    $ conda install pyms-agilent
