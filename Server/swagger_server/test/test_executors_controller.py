# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.executor import Executor  # noqa: E501
from swagger_server.models.post_executors import POSTExecutors  # noqa: E501
from swagger_server.test import BaseTestCase


class TestExecutorsController(BaseTestCase):
    """ExecutorsController integration test stubs"""

    def test_create_executor(self):
        """Test case for create_executor

        Creates an executor
        """
        body = POSTExecutors()
        response = self.client.open(
            '/RadonCTT/executors',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_executor_by_id(self):
        """Test case for get_executor_by_id

        Retrieve a executor
        """
        response = self.client.open(
            '/RadonCTT/executor/{executorId}'.format(executor_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_executors(self):
        """Test case for get_executors

        Get all executors
        """
        response = self.client.open(
            '/RadonCTT/executors',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
