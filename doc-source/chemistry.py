#!/usr/bin/env python3
#
#  chemistry.py
"""
Chemistry related sphinx extension.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Parts of the docstrings based on https://docutils.sourceforge.io/docs/howto/rst-roles.html
#

# stdlib
from typing import Any, Callable, Dict, Iterable, Optional, TypeVar

# 3rd party
import autodocsumm
from domdf_python_tools.stringlist import StringList
from sphinx.application import Sphinx
from sphinx.config import ENUM, Config


def validate_config(app: Sphinx, config: Config) -> None:
	r"""
	Validate the provided configuration values.

	:param app:
	:param config:
	:type config: :class:`~sphinx.config.Config`
	"""

	rst_prolog = StringList(config.rst_prolog)
	rst_prolog.append(".. |mz| replace:: :iabbr:`m/z (mass-to-charge ratio)`")
	config.rst_prolog = str(rst_prolog)


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app:

	:return:
	"""

	app.connect("config-inited", validate_config, priority=2000)

	return {
			# 'version': 'builtin',
			"parallel_read_safe": True,
			}
