MAX_CACHE_SIZE = 20
PATH_DELIMITERS = '/?#'
FRAGMENT_CHAR = '#'
QS_CHAR = '?'

_url_parse_cache = {}


class URIHelper(object):
	"""
	Object Returned when a URI is parsed
	"""

	def __init__(self, sch, auth, path, qs, frag):
		self.scheme = sch
		self.authority = auth
		self.path = path
		self.qs = qs
		self.fragment = frag

	def __repr__(self):
		return "URIHelper(scheme=\'%s\', authority=\'%s\', path=\'%s\', qs=\'%s\', fragment=\'%s\')" \
				% (self.scheme, self.authority, self.path, self.qs, self.fragment)
	
	def rebuild(self):
		url = ''
		if self.scheme:
			url += self.scheme + ':'
		if self.authority:
			url += '//' + self.authority
		url += self.path
		if self.qs:
			url += '?' + self.qs
		if self.fragment:
			url += '#' + fragment
		return url

	def parse_qs(self):
		variables = [v.split(';', 1) for v in self.qs.split('&', 1)]
		return {name: value for (name, value) in [v.split('=', 1) for v in variables]}


def _split_hierarchical_part(part):
	pos = len(part)
	for c in part:
		if c in PATH_DELIMITERS:
			pos = part.find(c)
			break
	return part[:pos], part[pos:]


def parse(url):
	# Check if we parsed this url already
	cached = _url_parse_cache.get(url)
	if cached:
		return cached
	if len(_url_parse_cache) >= MAX_CACHE_SIZE:
		_url_parse_cache.clear()

	scheme = authority = path = qs = fragment = ''

	# Find the scheme
	col = url.find(':')
	if col:
		scheme, rest = url[:col], url[col+1:]
		if rest[:2] == '//':
			authority, rest = _split_hierarchical_part(rest[2:])
		if FRAGMENT_CHAR in rest:
			rest, fragment = url.split(FRAGMENT_CHAR, 1)
		if QS_CHAR in rest:
			rest, qs = url.split(QS_CHAR, 1)
		path = rest
		return URIHelper(scheme, authority, path, qs, fragment)




