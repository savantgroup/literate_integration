"""Tests for the response matcher."""

from unittest import TestCase

from literate_integration.matcher import (
    Matcher,
    MatcherException,
    assertMatches,
)


class MatcherTestCase(TestCase):
    """Tests for the matcher."""

    def test_terminals_matched_exactly(self):
        string_terminal = 'asonthu'
        self.assertTrue(Matcher(string_terminal).matches(string_terminal))
        self.assertFalse(Matcher(string_terminal).matches(''))

        int_terminal = 325
        self.assertTrue(Matcher(int_terminal).matches(int_terminal))
        self.assertFalse(Matcher(int_terminal).matches(int_terminal + 1))

        float_terminal = 39.23
        self.assertTrue(Matcher(float_terminal).matches(float_terminal))
        self.assertFalse(Matcher(float_terminal).matches(float_terminal - 1))

        bool_terminal = False
        self.assertTrue(Matcher(bool_terminal).matches(bool_terminal))
        self.assertFalse(Matcher(bool_terminal).matches(not bool_terminal))

        null_terminal = None
        self.assertTrue(Matcher(null_terminal).matches(null_terminal))
        self.assertFalse(Matcher(null_terminal).matches(''))

    def test_same_lists_match(self):
        self.assertTrue(Matcher(['a']).matches(['a']))

    def test_original_as_sublist_matches(self):
        self.assertTrue(Matcher(['a']).matches(['a', 'b']))
        self.assertFalse(Matcher(['a']).matches(['b']))

    def test_same_dicts_match(self):
        self.assertTrue(Matcher({'a': 1}).matches({'a': 1}))

    def test_original_as_subset_matches(self):
        self.assertTrue(Matcher({'a': 1}).matches({'a': 1, 'b': 2}))
        self.assertFalse(Matcher({'a': 1}).matches({'b': 2}))
        self.assertFalse(Matcher({'a': 1}).matches({'a': 2, 'b': 2}))

    def test_non_supported_types_raise_exceptions(self):
        class Dummy(object):

            def __str__(self):
                return '"A dummy value"'

        with self.assertRaises(Exception):
            Matcher(Dummy()).matches(Dummy())

    def test_matcher_preserves_context(self):
        """Ensure that using the assertion method preserves context."""
        # The matcher should preserve the context from each
        # level.
        try:
            assertMatches({'a': [{'b': 1}]}, {'a': [{'b': 2}]})
        except MatcherException as mex:
            message = mex.message
        self.assertTrue(
            len(message) > 0
        )
        self.assertTrue('In dict' in message)
