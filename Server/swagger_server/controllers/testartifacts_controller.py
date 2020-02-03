import connexion
import six

from swagger_server.models.post_testartifacts import POSTTestartifacts  # noqa: E501
from swagger_server.models.testartifact import Testartifact  # noqa: E501
from swagger_server import util

from radonCTT.handlers.testartifacts import createTestartifact, getTestArtifactById, getTestArtifacts, downloadTestartifactById


def create_testartifact(body=None):  # noqa: E501
    """Creates a testartifact

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = POSTTestartifacts.from_dict(connexion.request.get_json())  # noqa: E501
    return createTestartifact(body)

    
def download_testartifact_by_id(testartifact_id):  # noqa: E501
    """Downloads the generated testartifact

     # noqa: E501

    :param testartifact_id: Id of testartifact to download
    :type testartifact_id: int

    :rtype: str
    """
    return downloadTestartifactById(testartifact_id)


def get_testartifact_by_id(testartifact_id):  # noqa: E501
    """Retrieve a testartifact

     # noqa: E501

    :param testartifact_id: Id of testartifact to return
    :type testartifact_id: int

    :rtype: Testartifact
    """
    return getTestArtifactById(testartifact_id)


def get_testartifacts():  # noqa: E501
    """Get all testartifacts

     # noqa: E501


    :rtype: List[Testartifact]
    """
    return getTestArtifacts()
