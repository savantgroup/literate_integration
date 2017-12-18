"""Test helper functions for generating documentation.

We don't really need to test the actual documentation
generation so much, since it's mostly just template
boilerplate. (I.e. constants.)

"""
from unittest import TestCase

from literate_integration.document import (
    get_leading_whitespace,
    remove_leading_whitespace,
    wrap_curl,
    MAX_LENGTH,
)


class LeadingWhitespaceTests(TestCase):
    """Tests helper functions."""

    def test_0_without_leading_whitespace(self):
        """Make sure there no leading whitespace doesn't fail."""
        self.assertEqual(
            get_leading_whitespace('Something without whitespace'),
            0,
        )

    def test_4_spaces_returns_4(self):
        """Ensure spaces are returned by count."""
        self.assertEqual(
            get_leading_whitespace(' ' * 4 + 'Indented 4 spaces'),
            4,
        )

    def test_remove_2_spaces(self):
        """Remove 2 spaces from the beginning of each line."""
        text = [
            '  This is the first line.',
            '  This is the second.',
        ]
        expected_text = [
            'This is the first line.',
            'This is the second.',
        ]
        self.assertEqual(
            remove_leading_whitespace(text),
            expected_text,
        )

    def test_inner_indentation_preserved(self):
        text = [
            '    This is the first line.',
            '        This is more indented.',
        ]
        expected_text = [
            'This is the first line.',
            '    This is more indented.',
        ]
        self.assertEqual(
            remove_leading_whitespace(text),
            expected_text,
        )


class CurlTests(TestCase):
    """Tests on the formatting of curl examples."""

    def test_wrap_curl_doesnt_change_if_under_MAX_LENGTH(self):
        curl = 'curl -H "Content-Type: application/json"'
        self.assertTrue(len(curl) < MAX_LENGTH)
        self.assertEqual(curl, wrap_curl(curl))

    def test_wrap_lines_over_max_length(self):
        content_type = '-H "Content-Type: ' + 'a' * MAX_LENGTH + '"'
        token = '-H "Authorization: Token asonetuanotehu'
        curl = 'curl {} {}'.format(
            content_type,
            token,
        )
        wrapped_curl = '\n'.join([
            'curl {}'.format(content_type),
            '     {}'.format(token),
        ])
        self.assertEqual(
            wrap_curl(curl),
            wrapped_curl,
            '\n\nExpected:\n{}\n\n But got:\n{}\n\n'.format(
                wrapped_curl,
                wrap_curl(curl)
            )
        )

    def test_with_data(self):
        data = (
            '\'{"temperature": 100.0, "density_value": 0.5, '
            '"absolute_viscosity": 10.0, "kinematic_viscosity": 40.0, '
            '"reference_type": 1}\''
        )
        curl = 'curl -X POST -d ' + data
        self.assertTrue(len(curl) > MAX_LENGTH)
        wrapped_curl = '\n'.join([
            'curl -X POST',
            '     -d ' + data,
        ])
        self.assertEqual(
            wrap_curl(curl),
            wrapped_curl,
            '\n\nExpected:\n{}\n\n But got:\n{}\n\n'.format(
                wrapped_curl,
                wrap_curl(curl)
            )
        )
