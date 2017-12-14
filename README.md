# Literate Integration

*A library for creating literate unit tests.*

## Purpose

To create documentation for REST backends which can be automatically
checked for validity.

## Installation

1. `cd` to the directory where you would like it to be installed.
2. Clone the repository locally, and use pip to install:
    ```
    git clone <url-to-repository>
    pip install literate_integration
    ```

## Use

### Defining Literate Tests

The following example will use *django-rest-framework* as an example
for the test-runner, client, etc.

To create a literate test for a rest endpoint, subclass `LiterateRESTTest`
and define the required properties. (The tests will fail if they are not
defined.)  For example, the following will perform a `GET` request on the
`/api/books/` endpoint using *django-rest-framework*'s `APIClient`:

```
from rest_framework.test import APITestCase, APIClient
from literate_integration.models import LiterateRESTTest

class GetBookList(LiterateRESTTest):
    """Get all the books in the library.

    Only books which are currently available at the physical
    location will be listed.  Books on loan can be gotten from
    the `/api/books/onloan/` endpoint.

    """

    data = None
    url = '/api/books/'
    request_function = APIClient().get
    request_method = 'GET'
    expected_data = {
        'count': 3,
    }
    expected_status = 200

```


### Running Literate Tests

To run the test, you need to generate a test class from the subclasses
of `LiterateRESTTest`.  In the same file where you specified your
`LiterateRESTTest`s, you can add the following lines:

```
import sys

...
# LiterateRESTTest subclasses
...

current_module = sys.modules[__name__]
BookTests = rest_test_factory(
    current_module,
    'BookTests',
    BaseClient=APITestCase,
)
```

Alternatively, you could define your literate tests in multiple files, then
add all of the tests in a single test file.  For example, if we have the
following directory structure:

```
my_library/
├──docs/
└──integration_tests/
   ├── book_tests.py
   ├── library_tests.py
   └── tests.py
```

Where *book_test.py* and *library_tests.py* contain your literate tests,
then you could have the following in *tests.py*:

```
from rest_framework.test import APITestCase
from literate_integration.factories import rest_test_factory

import .book_tests
import .library_tests

BookTests = rest_test_factory(
    book_tests,
    'BookTests',
    BaseClient=APITestCase,
)
LibraryTests = rest_test_factory(
    library_tests,
    'LibraryTests',
    BaseClient=APITestCase,
)
```

### Generating Documentation

To generate documentation, supply file names to the console script, `docgen`.
`docgen` will output the generated documentation from the files to standard
out.  For example, using the above file structure, we could generate documentation
as follows (from the root of the project, in *my_library*):

```
docgen integration_tests/book_tests.py integration_tests/library_tests.py \
  > docs/endpoint_documentation.md
```
