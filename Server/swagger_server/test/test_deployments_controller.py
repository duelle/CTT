# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.deployment import Deployment  # noqa: E501
from swagger_server.models.post_deployments import POSTDeployments  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDeploymentsController(BaseTestCase):
    """DeploymentsController integration test stubs"""

    def test_create_deployment(self):
        """Test case for create_deployment

        Creates a deployment
        """
        body = POSTDeployments()
        response = self.client.open(
            '/RadonCTT/deployments',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_deployment_by_id(self):
        """Test case for get_deployment_by_id

        Retrieve a deployment
        """
        response = self.client.open(
            '/RadonCTT/deployment/{deploymentId}'.format(deployment_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_deployments(self):
        """Test case for get_deployments

        Get all deployments
        """
        response = self.client.open(
            '/RadonCTT/deployments',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
