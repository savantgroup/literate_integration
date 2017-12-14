"""Defines an abstract class for performing literate tests."""

import abc


class LiterateRESTTest(abc.ABC):
    """A literate test.

    This abstract class should be subclassed for two purposes:
    - to run integration tests on a REST endpoint
    - to generate documentation on the endpoints.

    The class docstring will be used as a description of the
    request that is sent, while the properties below are included
    as examples of the sort of request which can be sent.

    """

    @abc.abstractproperty
    def data(self):
        """The payload to send to the endpoint."""
        ...

    @abc.abstractproperty
    def url(self):
        """The url to hit."""
        ...

    @abc.abstractproperty
    def request_function(self):
        """A function which executes the request.

        This function must return a response object which
        has the members, `content` and `status_code`, and
        which has the method, `json` defined. (That returns the
        json for the request.)

        """
        ...

    @abc.abstractproperty
    def request_method(self):
        """The method that the request_function performs.

        It should be one of POST, GET, PATCH, PUT, or DELETE.

        """
        ...

    @abc.abstractproperty
    def expected_data(self):
        """The data we expect back from the endpoint.

        Only the keys present in expected_data will be tested.
        So, if you don't want to test certain keys (such as `id`),
        then don't add them to the test.

        """
        ...

    @abc.abstractproperty
    def expected_status(self):
        """The status of the response we expect."""
        ...
