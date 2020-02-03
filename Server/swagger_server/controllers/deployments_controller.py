import connexion
import six

from swagger_server.models.deployment import Deployment  # noqa: E501
from swagger_server.models.post_deployments import POSTDeployments  # noqa: E501
from swagger_server import util

from radonCTT.handlers.deployments import createDeployment, getDeploymentById, getDeployments


def create_deployment(body=None):  # noqa: E501
    """Creates a deployment

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = POSTDeployments.from_dict(connexion.request.get_json())  # noqa: E501
    return createDeployment(body)


def get_deployment_by_id(deployment_id):  # noqa: E501
    """Retrieve a deployment

     # noqa: E501

    :param deployment_id: Id of deployment to return
    :type deployment_id: int

    :rtype: Deployment
    """
    return getDeploymentById(deployment_id)


def get_deployments():  # noqa: E501
    """Get all deployments

     # noqa: E501


    :rtype: List[Deployment]
    """
    return getDeployments()
