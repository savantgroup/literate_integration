"""Define a matcher for tests."""
from collections import deque


# A global context store.  This will track the context of
# the matcher during its runtime.
_context = deque()


def _add_context(context):
    global _context
    _context.append(context)


def _remove_context():
    global _context
    _context.pop()


def _get_context():
    global _context
    return _context


def _reset_context():
    global _context
    _context = deque()


def is_terminal(value):
    return (isinstance(value, float)
            or isinstance(value, int)
            or isinstance(value, bool)
            or isinstance(value, str)
            or value is None
            )


class _TerminalMatcher(object):
    """Matches a terminal value."""

    def __init__(self, value):
        assert(is_terminal(value))
        self.original = value

    def matches(self, value):
        if not self.original == value:
            _add_context(
                'Expected {} but received {}'.format(self.original, value)
            )
            return False
        return True


class _ListMatcher(object):
    """Matches a list value."""

    def __init__(self, values):
        assert(isinstance(values, list))
        self.matchers = map(Matcher, values)

    def matches(self, values):
        _add_context('In list')
        if not isinstance(values, list):
            _add_context(
                'Expected List but got {}'.format(values)
            )
            return False
        for matcher in self.matchers:
            if not any([matcher.matches(value) for value in values]):
                return False
        _remove_context()
        return True


class _DictMatcher(object):
    """Matches a dictionary value."""

    def __init__(self, values):
        assert(isinstance(values, dict))
        self.matchers = {
            key: Matcher(value) for key, value in values.items()
        }

    def matches(self, value):
        _add_context('In dict')
        if not isinstance(value, dict):
            return False
        for key, matcher in self.matchers.items():
            _add_context('For key {}'.format(key))
            if key not in value:
                _add_context('Key was not present')
                return False
            if not matcher.matches(value[key]):
                return False
        _remove_context()
        return True


class Matcher(object):
    """Tells if response objects match.

    The Matcher can match against terminal values (strings,
    floats, integers, or booleans), or against composite values
    (lists, dictionaries.)

    Terminal values much match exactly.  Composite values must have
    at least one instance which satisfies the matcher.

    """

    def __init__(self, value):
        """Create a new matcher instance.

        Args:
            value: The value we would like to match against.
                This can be a terminal value or composite value.

        """
        if is_terminal(value):
            self.matcher = _TerminalMatcher(value)
        elif isinstance(value, list):
            self.matcher = _ListMatcher(value)
        elif isinstance(value, dict):
            self.matcher = _DictMatcher(value)
        else:
            raise Exception('Unsupported comparision type {}:{}'.format(
                value,
                value.__class__.__name__
            ))

    def matches(self, value):
        """Return true if this value matches the original."""
        return self.matcher.matches(value)


# Below is defined a convenience method for passing on the context
# for a single call.  That context is passed through an exception.

class MatcherException(Exception):

    def __init__(self, message=''):
        self.message = message


def assertMatches(expected, actual):
    """Run the given check, raising an exception if it fails."""
    _reset_context()
    if not Matcher(expected).matches(actual):
        raise MatcherException(': '.join(_get_context()))
