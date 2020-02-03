# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.result import Result  # noqa: E501
from swagger_server.test import BaseTestCase


class TestResultsController(BaseTestCase):
    """ResultsController integration test stubs"""

    def test_get_result_by_id(self):
        """Test case for get_result_by_id

        Retrieve a result
        """
        response = self.client.open(
            '/RadonCTT/result/{resultId}'.format(result_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_results(self):
        """Test case for get_results

        Get all results
        """
        response = self.client.open(
            '/RadonCTT/results',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
