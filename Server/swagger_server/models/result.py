# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Result(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, project_id: int=None, testartifact_id: int=None, result_path: str=None):  # noqa: E501
        """Result - a model defined in Swagger

        :param id: The id of this Result.  # noqa: E501
        :type id: int
        :param project_id: The project_id of this Result.  # noqa: E501
        :type project_id: int
        :param testartifact_id: The testartifact_id of this Result.  # noqa: E501
        :type testartifact_id: int
        :param result_path: The result_path of this Result.  # noqa: E501
        :type result_path: str
        """
        self.swagger_types = {
            'id': int,
            'project_id': int,
            'testartifact_id': int,
            'result_path': str
        }

        self.attribute_map = {
            'id': 'id',
            'project_id': 'projectId',
            'testartifact_id': 'testartifactId',
            'result_path': 'resultPath'
        }
        self._id = id
        self._project_id = project_id
        self._testartifact_id = testartifact_id
        self._result_path = result_path

    @classmethod
    def from_dict(cls, dikt) -> 'Result':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Result of this Result.  # noqa: E501
        :rtype: Result
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Result.


        :return: The id of this Result.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Result.


        :param id: The id of this Result.
        :type id: int
        """

        self._id = id

    @property
    def project_id(self) -> int:
        """Gets the project_id of this Result.


        :return: The project_id of this Result.
        :rtype: int
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id: int):
        """Sets the project_id of this Result.


        :param project_id: The project_id of this Result.
        :type project_id: int
        """

        self._project_id = project_id

    @property
    def testartifact_id(self) -> int:
        """Gets the testartifact_id of this Result.


        :return: The testartifact_id of this Result.
        :rtype: int
        """
        return self._testartifact_id

    @testartifact_id.setter
    def testartifact_id(self, testartifact_id: int):
        """Sets the testartifact_id of this Result.


        :param testartifact_id: The testartifact_id of this Result.
        :type testartifact_id: int
        """

        self._testartifact_id = testartifact_id

    @property
    def result_path(self) -> str:
        """Gets the result_path of this Result.


        :return: The result_path of this Result.
        :rtype: str
        """
        return self._result_path

    @result_path.setter
    def result_path(self, result_path: str):
        """Sets the result_path of this Result.


        :param result_path: The result_path of this Result.
        :type result_path: str
        """

        self._result_path = result_path