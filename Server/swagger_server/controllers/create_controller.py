import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.create_job import CreateJob  # noqa: E501
from swagger_server import util


def create_job(body=None):  # noqa: E501
    """Create a new testing job.

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponse
    """
    if connexion.request.is_json:
        body = CreateJob.from_dict(connexion.request.get_json())  # noqa: E501
        
    return 'do some magic!'
