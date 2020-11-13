# BSD Licensed
# https://github.com/quiver/sphinx-ext-wikipedia
"""
Sphinx extension to create links to Wikipedia articles.

:wikipedia:`Sphinx`

:wikipedia:`mythical creature <Sphinx>`

:wikipedia:`:zh:斯芬克斯`

:wikipedia:`Answer to the Ultimate Question of Life, the Universe, and Everything <:de:42 (Antwort)>`
"""

# stdlib
import re
from typing import Dict, List, Sequence, Tuple, Union
from urllib.parse import quote

# 3rd party
from docutils import nodes, utils
from docutils.nodes import system_message
from docutils.parsers.rst.states import Inliner
from sphinx import addnodes
from sphinx.util.nodes import split_explicit_title

base_url = "https://%s.wikipedia.org/wiki/"


def make_wikipedia_link(
		name: str,
		rawtext: str,
		text: str,
		lineno: int,
		inliner: Inliner,
		options: Dict = {},
		content: List[str] = []
		) -> Tuple[Sequence[Union[nodes.reference, addnodes.only]], List[system_message]]:
	"""
	Adds a link to the given article on :wikipedia:`Wikipedia`.

	:param name: The local name of the interpreted role, the role name actually used in the document.
	:param rawtext: A string containing the entire interpreted text input, including the role and markup.
	:param text: The interpreted text content.
	:param lineno: The line number where the interpreted text begins.
	:param inliner: The :class:`docutils.parsers.rst.states.Inliner` object that called :func:`~.source_role`.
		It contains the several attributes useful for error reporting and document tree access.
	:param options: A dictionary of directive options for customization (from the ``role`` directive),
		to be interpreted by the function.
		Used for additional attributes for the generated elements and other functionality.
	:param content: A list of strings, the directive content for customization (from the ``role`` directive).
		To be interpreted by the function.

	:return: A list containing the created node, and a list containing any messages generated during the function.
	"""

	env = inliner.document.settings.env
	lang = env.config.wikipedia_lang

	text = utils.unescape(text)
	has_explicit, title, target = split_explicit_title(text)

	m = re.match(r':(.*?):(.*)', target)
	if m:
		lang, target = m.groups()
		if not has_explicit:
			title = target

	ref = base_url % lang + quote(target.replace(' ', '_').encode("utf8"), safe='')

	node = nodes.reference(rawtext, title, refuri=ref, **options)
	return [node], []


def setup(app):
	app.add_config_value("wikipedia_lang", "en", "env")
	app.add_role("wikipedia", make_wikipedia_link)
