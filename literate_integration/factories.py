"""Define a function which can run integration tests."""

from unittest import TestCase

import inspect
import re

from .models import LiterateRESTTest


CAPITALS = re.compile('[A-Z]')


def _to_snake_case(name):
    uppers = CAPITALS.findall(name)
    # The first string will be blank -- it should start with a capital.
    lowers = CAPITALS.split(name)[1:]
    new_name = '_'.join([
        ''.join([x.lower(), y]) for x, y in zip(uppers, lowers)
    ])
    if new_name.startswith('test_'):
        return new_name
    return 'test_' + new_name


def _get_rest_test(klass):
    def inner(self):
        instance = klass()
        instance.setUp()
        response = klass.request_function(
            instance.url,
            data=instance.data,
        )
        self.assertEqual(
            response.status_code,
            instance.expected_status,
            response.content
        )
        data = response.json()
        for key, value in instance.expected_data.items():
            self.assertTrue(
                key in data,
                'The key "{}" was not present in the response.'.format(
                    key
                )
            )
            self.assertEqual(
                data[key], value,
                'The value for "{}" should have been {}, but was {}'.format(
                    key, value, data[key]
                )
            )
    return inner


def rest_test_factory(module, class_name, BaseClass=TestCase):
    """Get a test class for the given module.

    Args:
        module: The module which holds the classes.
        name: The name the integration test case should have.
        BaseClass: The base class for this test.  Normally, this
            will probably be rest_framework's APITestCase, but
            it doesn't have to be.  However, it _must_ have the
            method `assertEqual` and `assertTrue` defined.

    Returns:
        A single integration test containing all of the
        tests defined in the module.

    """

    def __init__(self, *args, **kwargs):
        # return BaseClass.__init__(self, name[:-len('Class')])
        return BaseClass.__init__(self, *args, **kwargs)

    tests = inspect.getmembers(module, inspect.isclass)

    # Make sure all the tests follow the pattern.
    for name, klass in tests:
        if inspect.isabstract(klass):
            continue
        if not issubclass(klass, LiterateRESTTest):
            continue
        klass()

    # Make the tests
    fns = {
        _to_snake_case(name): _get_rest_test(klass)
        for name, klass in tests
        if (issubclass(klass, LiterateRESTTest)
            and 'LiterateRESTTest' not in name)
    }
    fns['__init__'] = __init__
    testClass = type(class_name, (BaseClass,), fns)
    return testClass
