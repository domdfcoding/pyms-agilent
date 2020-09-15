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


def add_autosummary(self):
	"""
	Add the :rst:dir:`autosummary` table of this documenter.
	"""

	if not self.options.autosummary:
		return

	content = StringList()
	sourcename = self.get_sourcename()
	grouped_documenters = self.get_grouped_documenters()

	for section, documenters in grouped_documenters.items():
		if not self.options.autosummary_no_titles:
			content.append(f'**{section}:**')

		content.blankline(ensure_single=True)

		content.append('.. autosummary::')
		content.blankline(ensure_single=True)

		member_order = get_first_matching(
				lambda x: x != "groupwise",
				[
						self.options.member_order,
						self.env.config.autodoc_member_order,
						self.env.config.autodocsumm_member_order,
						],
				default="alphabetical",
				)

		with content.with_indent_size(content.indent_size + 1):
			for documenter, _ in self.sort_members(documenters, member_order):
				content.append(f"~{documenter.fullname}")

		content.blankline()

	for line in content:
		self.add_line(line, sourcename)


_T = TypeVar("_T")
no_default = object()


class NoMatchError(ValueError):
	"""
	Raised when no matching values were found in :func:`~.get_first_matching`.
	"""


def get_first_matching(
		condition: Callable[[_T], bool],
		iterable: Iterable[_T],
		default: Optional[_T] = no_default,  # type: ignore
		) -> _T:
	"""
	Returns the first value in ``iterable`` that meets ``condition``, or ``default`` if none match.

	:param condition:
	:param iterable:
	:param default:
	"""

	if default is not no_default:
		if not condition(default):
			raise ValueError("The condition must evaluate to True for the default value.")

		iterable = [*iterable, default]

	for match in iterable:
		if condition(match):
			return match

	raise NoMatchError(f"No matches values for '{condition}' in {iterable}")


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app:

	:return:
	"""

	app.connect("config-inited", validate_config, priority=2000)
	autodocsumm.AutosummaryDocumenter.add_autosummary = add_autosummary
	app.add_config_value(
			'autodocsumm_member_order',
			'alphabetical',
			True,
			ENUM('alphabetic', 'alphabetical', 'bysource'),
			)

	return {
			# 'version': 'builtin',
			'parallel_read_safe': True,
			'parallel_write_safe': True,
			}
