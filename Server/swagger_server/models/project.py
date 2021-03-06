# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Project(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, status: str=None, repository_url: str=None, servicetemplate_location: str=None, project_path: str=None):  # noqa: E501
        """Project - a model defined in Swagger

        :param id: The id of this Project.  # noqa: E501
        :type id: int
        :param status: The status of this Project.  # noqa: E501
        :type status: str
        :param repository_url: The repository_url of this Project.  # noqa: E501
        :type repository_url: str
        :param servicetemplate_location: The servicetemplate_location of this Project.  # noqa: E501
        :type servicetemplate_location: str
        :param project_path: The project_path of this Project.  # noqa: E501
        :type project_path: str
        """
        self.swagger_types = {
            'id': int,
            'status': str,
            'repository_url': str,
            'servicetemplate_location': str,
            'project_path': str
        }

        self.attribute_map = {
            'id': 'id',
            'status': 'status',
            'repository_url': 'repositoryUrl',
            'servicetemplate_location': 'servicetemplateLocation',
            'project_path': 'projectPath'
        }
        self._id = id
        self._status = status
        self._repository_url = repository_url
        self._servicetemplate_location = servicetemplate_location
        self._project_path = project_path

    @classmethod
    def from_dict(cls, dikt) -> 'Project':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Project of this Project.  # noqa: E501
        :rtype: Project
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Project.


        :return: The id of this Project.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Project.


        :param id: The id of this Project.
        :type id: int
        """

        self._id = id

    @property
    def status(self) -> str:
        """Gets the status of this Project.


        :return: The status of this Project.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this Project.


        :param status: The status of this Project.
        :type status: str
        """

        self._status = status

    @property
    def repository_url(self) -> str:
        """Gets the repository_url of this Project.


        :return: The repository_url of this Project.
        :rtype: str
        """
        return self._repository_url

    @repository_url.setter
    def repository_url(self, repository_url: str):
        """Sets the repository_url of this Project.


        :param repository_url: The repository_url of this Project.
        :type repository_url: str
        """

        self._repository_url = repository_url

    @property
    def servicetemplate_location(self) -> str:
        """Gets the servicetemplate_location of this Project.


        :return: The servicetemplate_location of this Project.
        :rtype: str
        """
        return self._servicetemplate_location

    @servicetemplate_location.setter
    def servicetemplate_location(self, servicetemplate_location: str):
        """Sets the servicetemplate_location of this Project.


        :param servicetemplate_location: The servicetemplate_location of this Project.
        :type servicetemplate_location: str
        """

        self._servicetemplate_location = servicetemplate_location

    @property
    def project_path(self) -> str:
        """Gets the project_path of this Project.


        :return: The project_path of this Project.
        :rtype: str
        """
        return self._project_path

    @project_path.setter
    def project_path(self, project_path: str):
        """Sets the project_path of this Project.


        :param project_path: The project_path of this Project.
        :type project_path: str
        """

        self._project_path = project_path
