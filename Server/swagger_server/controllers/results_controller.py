import connexion
import six

from swagger_server.models.result import Result  # noqa: E501
from swagger_server import util

from radonCTT.handlers.results import downloadResultById, getResultById, getResults


def download_result_by_id(result_id):  # noqa: E501
    """Downloads the generated results

     # noqa: E501

    :param result_id: Id of result to download
    :type result_id: int

    :rtype: str
    """
    return downloadResultById(result_id)


def get_result_by_id(result_id):  # noqa: E501
    """Retrieve a result

     # noqa: E501

    :param result_id: Id of Result to return
    :type result_id: int

    :rtype: Result
    """
    return getResultById(result_id)


def get_results():  # noqa: E501
    """Get all results

     # noqa: E501


    :rtype: List[Result]
    """
    return getResults()