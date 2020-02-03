# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.post_projects import POSTProjects  # noqa: E501
from swagger_server.models.project import Project  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProjectsController(BaseTestCase):
    """ProjectsController integration test stubs"""

    def test_create_project(self):
        """Test case for create_project

        Creates a project
        """
        body = POSTProjects()
        response = self.client.open(
            '/RadonCTT/projects',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_project(self):
        """Test case for delete_project

        Delete a project
        """
        response = self.client.open(
            '/RadonCTT/project/{projectId}'.format(project_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_project_by_id(self):
        """Test case for get_project_by_id

        Retrieve a project
        """
        response = self.client.open(
            '/RadonCTT/project/{projectId}'.format(project_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_projects(self):
        """Test case for get_projects

        Get a list of projects
        """
        response = self.client.open(
            '/RadonCTT/projects',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
