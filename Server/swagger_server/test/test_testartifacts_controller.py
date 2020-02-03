# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.post_testartifacts import POSTTestartifacts  # noqa: E501
from swagger_server.models.testartifact import Testartifact  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTestartifactsController(BaseTestCase):
    """TestartifactsController integration test stubs"""

    def test_create_testartifact(self):
        """Test case for create_testartifact

        Creates a testartifact
        """
        body = POSTTestartifacts()
        response = self.client.open(
            '/RadonCTT/testartifacts',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_testartifact_by_id(self):
        """Test case for get_testartifact_by_id

        Retrieve a testartifact
        """
        response = self.client.open(
            '/RadonCTT/testartifact/{testartifactId}'.format(testartifact_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_testartifacts(self):
        """Test case for get_testartifacts

        Get all testartifacts
        """
        response = self.client.open(
            '/RadonCTT/testartifacts',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
