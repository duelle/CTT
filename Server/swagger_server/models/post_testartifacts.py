# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class POSTTestartifacts(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, project_id: int=None):  # noqa: E501
        """POSTTestartifacts - a model defined in Swagger

        :param project_id: The project_id of this POSTTestartifacts.  # noqa: E501
        :type project_id: int
        """
        self.swagger_types = {
            'project_id': int
        }

        self.attribute_map = {
            'project_id': 'projectId'
        }
        self._project_id = project_id

    @classmethod
    def from_dict(cls, dikt) -> 'POSTTestartifacts':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The POSTTestartifacts of this POSTTestartifacts.  # noqa: E501
        :rtype: POSTTestartifacts
        """
        return util.deserialize_model(dikt, cls)

    @property
    def project_id(self) -> int:
        """Gets the project_id of this POSTTestartifacts.


        :return: The project_id of this POSTTestartifacts.
        :rtype: int
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id: int):
        """Sets the project_id of this POSTTestartifacts.


        :param project_id: The project_id of this POSTTestartifacts.
        :type project_id: int
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id
