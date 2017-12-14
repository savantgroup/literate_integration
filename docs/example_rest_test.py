"""An example of using literate integration tests."""

import sys
import requests

from literate_integration.models import LiterateRESTTest
from literate_integration.runner import rest_test_factory


class CreateSampleInLuna(LiterateRESTTest):
    """To create a sample in Luna, you will need the following
    information:

      - The brand name of the sample.
      - The supplier of the sample.

    """

    url = 'http://localhost:8000/api/samples/'

    request_function = requests.get

    data = {
        'brand_name': 'Pennzoil',
        'supplier': 'Acme Co.',
    }

    expected_data = {
        'id': int,
        'brand_name': 'Pennzoil',
        'supplier': 'Acme Co.',
    }

    expected_status = 201


current_module = sys.modules[__name__]
SampleTests = rest_test_factory(current_module, 'SampleTests')
