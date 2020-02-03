import connexion
import six

from swagger_server.models.executor import Executor  # noqa: E501
from swagger_server.models.post_executors import POSTExecutors  # noqa: E501
from swagger_server import util

from radonCTT.handlers.executors import createExecutor, getExecutorById, getExecutors


def create_executor(body=None):  # noqa: E501
    """Creates an executor

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = POSTExecutors.from_dict(connexion.request.get_json())  # noqa: E501
    return createExecutor(body)


def get_executor_by_id(executor_id):  # noqa: E501
    """Retrieve a executor

     # noqa: E501

    :param executor_id: Id of executor to return
    :type executor_id: int

    :rtype: Executor
    """
    return getExecutorById(executor_id)


def get_executors():  # noqa: E501
    """Get all executors

     # noqa: E501


    :rtype: List[Executor]
    """
    return getExecutors()
