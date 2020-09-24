#  From https://github.com/jondot/attrs-serde
#  MIT License
#
#  Copyright (c) 2019 Dotan Nahum
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
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

try:
	# 3rd party
	from cytoolz.curried import filter, get_in, map, pipe, reduce, update_in
except ImportError:
	from toolz.curried import get_in, update_in, reduce, pipe, map, filter

# 3rd party
from attr import asdict, fields

__all__ = ["serde"]


def serde(cls=None, from_key="from", to_key="to"):
	"""
	Decorator to add serialisation and deserialisation capabilities to attrs classes.

	:param cls:
	:param from_key:
	:param to_key:

	:return:
	"""

	def serde_with_class(cls):
		from_fields = list(map(lambda a: (a, get_in([from_key], a.metadata, [a.name])), fields(cls)))

		to_fields = pipe(
				fields(cls),
				map(lambda a: (a, get_in([to_key], a.metadata))),
				filter(lambda f: f[1]),
				list,
				)

		def from_dict(d):
			return cls(**dict(map(
					lambda f: (f[0].name, get_in(f[1], d, f[0].default)),
					from_fields,
					)))

		def to_dict(self):
			d = asdict(self)
			if not to_fields:
				return d

			return reduce(
					lambda acc, f: update_in(acc, f[1], lambda _: d[f[0].name]),
					to_fields,
					{},
					)

		cls.from_dict = staticmethod(from_dict)
		cls.to_dict = to_dict
		return cls

	if cls:
		return serde_with_class(cls)
	else:
		return serde_with_class
