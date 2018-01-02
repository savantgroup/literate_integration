# Change Log

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.0.5]

### Changed

- URL will go on its own line, now, under two conditions: either the
  body of the request is wrapped, or the request and URL together
  are greater than the maximum length (currently 60.)

## [0.0.4]

### Added

- Add support for list response from an endpoint.  Previously, the
  expected data had to match a detail response. (That is, both the
  expected and actual data had to be dictionaries.) Now, both the
  expected data and actual data can be lists of dictionaries.
  The list response works by making sure there is at least one
  object in the actual response which matches all fields in each of
  the expected objects.  If this is not the case, then an exception
  is thrown.

  For example, if we have

```
  expected_data = [{'id': 1}, {'id': 3}]
```

  for `expected_data`, and we receive:

```
  [
    {
      "id": 1,
      "name": "Jerry",
    },
    {
      "id': 2,
      "name": "Bob",
    }
  ]
```

  Then the test would pass.  However, if we had

```
  expected_data = [{'id': 1}, {'id': 2, 'name': 'Alice'}]
```

  Then the test would fail, because the response doesn't contain
  any object which has both an `id` of 2 and a `name` of "Alice".

## [0.0.3]

### Added

- Add flag for [pandoc](http://pandoc.org/)-style classes for code
  examples, etc.  That way, if someone is converting the markdown
  into html using pandoc, then the code examples and headers can
  be easily styled.

## [0.0.2]

### Added

- Add generation of required setup from `setUp` method.  Used if the
  `LiterateRESTTest` subclass has a `setUp` method defined, and
  that `setUp` method has a docstring.  In this case, the docstring's
  third line and afterwards will be used and placed in a "Setup Required"
  section.

  For example, say we have a `LiterateRESTTest` like the following:

```
class MyLiterateTest(LiterateRESTTest):
    ...

    def setUp(self):
      """This line is ignored.

      This line is the first one which will be included in the
      documentation.

      """
      ...
```

- Add wrapping to the curl examples.  If the line of the curl example
  is more than 70 characters long, then each of the flags will be placed
  on their own lines.

- Add wrapping to the JSON data in curl examples.

## [0.0.1]

### Added

- `docgen`, a command-line script for generating documentation from
  the given literal test files.  It outputs markdown documentation to
  standard out.

  For example, the following will compile the example documentation
  for this library:

```
  docgen docs/example_rest_test.py > docs/api_documentation.md
```

  `docgen` does not work with Django.  The next iteration will add an
  equivalent Django management command.

- *Django* management command for `docgen`.  You can use `docgen` from
  Django by installing it, adding `"literate_integration"` to the
  `INSTALLED_APPS` in the settings file, and by calling it with

```
./manage.py docgen <files>
```

- `setUp()` function to perform a given action before a test is run.


## [0.0.0]

### Added

- `LiterateRESTTest`, an abstract class which can be subclassed to create
  literate integration tests for REST endpoints.  A `LiterateRESTTest`
  must include certain attributes which are necessary for demonstrating/
  testing the use of a given endpoint.

  See ![example_rest_test.py](docs/example_rest_test.py) for an example.

- `rest_test_factory`, a function for generating a REST test class from
  a subclass of `LiterateRESTTest`.

  See ![example_rest_test.py](docs/example_rest_test.py) for an example.

The above two additions are really intended to be used with
*django-rest-framework*, though they could possible be used elsewhere
(say, in a normal Django app, or a Flask application.)  If using with
*django-rest-framework*, though, the subclass of `LiterateRESTTest`
should use an `rest_framework.test.APIClient` instance's request method
for the `request_function` property.  Additionally, the `BaseClass`
parameter to `rest_test_factory` should be `rest_framework.test.APITestCase`.

For example:

```
from rest_framework.test import APITestCase, APIClient

from literate_integration.models import LiterateRESTTest
from literate_integration.factories import rest_test_factory

class BookAHotelRoom(LiterateRESTTest):
  """Booking a hotel room.

  Booking a hotel room requires a user id (see 'Get User Id').
  It also requires knowing which room to use (see 'Get Room Id').

  '"""
  ... # url, data, etc.
  request_function = APIClient().post

  ... # expected_data, expected_status, etc.

current_module = sys.modules[__name__]
RoomTests = rest_test_factory(
    current_module,
    'RoomTests',
    BaseClient=APITestCase,
)
```
