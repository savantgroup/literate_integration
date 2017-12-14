"""Tests literate REST tests."""

import inspect
from unittest import TestCase

from literate_integration.models import LiterateRESTTest
from literate_integration.factories import rest_test_factory

# -------------------- HELPERS


class MockResponse(object):

    def __init__(self, response_data, response_status):
        self.data = response_data
        self.status_code = response_status

    @property
    def content(self):
        return str(self.data)

    def json(self):
        return self.data


def get_mock_get(response_data, response_status):
    def mock_get(url, data):
        return MockResponse(response_data, response_status)
    return mock_get


class MockModule(object):

    def __init__(self, klass):
        setattr(self, klass.__name__, klass)

# -------------------- GOOD EXAMPLE


class GoodExampleTest(LiterateRESTTest):
    """This is an example of a literate rest test."""

    url = 'http://localhost:7000/api/some-data/'

    request_function = get_mock_get({'errors': 'It didn\'t work.'}, 400)
    request_method = 'GET'

    data = {
        'item1': 'value1',
        'item2': 'value2',
    }

    expected_data = {
        'id': 1,
        'item1': 'value1',
        'item2': 'value2',
    }

    expected_status = 200


class GoodExampleTestCase(TestCase):
    """Makes sure the good example will actually work."""

    def test_can_extract_docstring_representation(self):
        self.assertTrue('example of a literate' in GoodExampleTest.__doc__)

    def test_can_extract_data_expected_data_and_status(self):
        instance = GoodExampleTest()
        self.assertTrue('item1' in instance.data)
        self.assertTrue('id' in instance.expected_data)
        self.assertEqual(200, instance.expected_status)

    def test_can_be_passed_to_factory_for_test_class(self):
        mock_module = MockModule(GoodExampleTest)
        TestClass = rest_test_factory(mock_module, 'MyTest')
        self.assertTrue(
            issubclass(TestClass, TestCase),
            'By default, it should be a subclass of TestCase.'
        )
        instance = TestClass()
        methods = inspect.getmembers(instance, inspect.ismethod)
        tests = [
            x for x, y in methods
            if x.startswith('test_')
        ]
        good_example_test_found = False
        for method_name in tests:
            good_example_test_found |= 'test_good_example_test' in method_name
        self.assertTrue(
            good_example_test_found,
            'A method with a name associated with the class should '
            'have been present in the test class.'
        )


# -------------------- BAD EXAMPLE

class MissingDataTest(LiterateRESTTest):

    expected_data = ['something']
    expected_status = 200


class BadExamplesTestCase(TestCase):

    def test_missing_data_cant_instantiate(self):
        with self.assertRaises(Exception):
            MissingDataTest()
