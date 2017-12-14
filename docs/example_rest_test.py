"""An example of using literate integration tests."""

import sys

from literate_integration.models import LiterateRESTTest
from literate_integration.factories import rest_test_factory


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


class CreateSampleInLuna(LiterateRESTTest):
    """To create a sample in Luna, you will need the following
    information:

      - The brand name of the sample.
      - The supplier of the sample.

    """

    url = 'http://localhost:8000/api/samples/3'

    request_function = get_mock_get(
        {
            'id': 3,
            'brand_name': 'Pennzoil',
            'supplier': 'Acme Co.',
        },
        201,
    )
    request_method = 'GET'

    data = dict()

    expected_data = {
        'id': 3,
        'brand_name': 'Pennzoil',
        'supplier': 'Acme Co.',
    }

    expected_status = 201


current_module = sys.modules[__name__]
SampleTests = rest_test_factory(current_module, 'SampleTests')
