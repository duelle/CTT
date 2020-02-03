import connexion
import six

from swagger_server.models.post_projects import POSTProjects  # noqa: E501
from swagger_server.models.project import Project  # noqa: E501
from swagger_server import util

from radonCTT.handlers.projects import createProject, deleteProject, getProjectById, getProjects


def create_project(body=None):  # noqa: E501
    """Creates a project

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = POSTProjects.from_dict(connexion.request.get_json())  # noqa: E501
    return createProject(body)


def delete_project(project_id):  # noqa: E501
    """Delete a project

     # noqa: E501

    :param project_id: Id of project to delete
    :type project_id: int

    :rtype: None
    """
    return deleteProject(project_id)


def get_project_by_id(project_id):  # noqa: E501
    """Retrieve a project

     # noqa: E501

    :param project_id: Id of project to return
    :type project_id: int

    :rtype: Project
    """
    return getProjectById(project_id)


def get_projects():  # noqa: E501
    """Get a list of projects

     # noqa: E501


    :rtype: List[Project]
    """
    return getProjects()
