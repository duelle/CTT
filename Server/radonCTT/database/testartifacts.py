#==================================================================|
"""
Contains helper methods to get Testartifact objects from the database
"""
#==================================================================|

from swagger_server.models import Testartifact, Project

from radonCTT.database import databaseSession
from radonCTT.database.policytests import getPolicyTestsForTestartifact

#------------------------------------------------------|
def testartifactQueryToObject(testartifactQuery):
    """
    This helper method turns the response from the query
    into a propper Testartifact object. This way, all the 
    swagger stuff is initialized on the object.
    """

    testartifact = Testartifact(
        id=testartifactQuery.id,
        status= testartifactQuery.status,
        project_id=testartifactQuery.project_id,
    )

    if hasattr(testartifactQuery, 'policy_tests'):
        testartifact.policy_tests = testartifactQuery.policy_tests

    return testartifact
#------------------------------------------------------|

#------------------------------------------------------|
def updateTestartifact(testartifact : Testartifact):
    """
    Updates a Testartifact, but does not commit the changes
    """
    testartifactQuery = Testartifact.query.get(testartifact.id)
    
    testartifactQuery.status = testartifact.status
    testartifactQuery.project_id = testartifact.project_id

    databaseSession.flush()
#------------------------------------------------------|

#------------------------------------------------------|
def getTestartifact(testartifactId, isLazyLoad):
    """
    Returns Testartifact with given Id.

    Args:
        testartifacctId (int) : Id of testartifact to load
        isLazyLoad (bool) : Wether or not to lazy load relations
    """

    testartifactQuery = Testartifact.query.get(testartifactId)

    if isLazyLoad and testartifactQuery:
        testartifactQuery.policy_tests = getPolicyTestsForTestartifact(testartifactQuery.id)

    if testartifactQuery:
        return testartifactQueryToObject(testartifactQuery)
    else:
        return None
#------------------------------------------------------|

#------------------------------------------------------|
def getTestartifactForProject(project, isLazyLoad):
    """
    Returns Testartifact with given Id.

    Args:
        project (Project) : Project to retrieve the TA from
        isLazyLoad (bool) : Whether or not to lazy load relations
    """

    testartifactQuery = Testartifact.query.filter_by(_project_id = project.id).first()

    if isLazyLoad and testartifactQuery:
        testartifactQuery.policy_tests = getPolicyTestsForTestartifact(testartifactQuery.id)

    if testartifactQuery:
        return testartifactQueryToObject(testartifactQuery)
    else:
        return None
#------------------------------------------------------|

#------------------------------------------------------|
def getTestartifacts():
    """
    Returns all Testartifacts in the database
    """

    testartifactQueries = Testartifact.query.all()
    
    if testartifactQueries:   
        testartifactList = []
        for testartifactQuery in testartifactQueries:
            testartifactList.append(testartifactQueryToObject(testartifactQuery))
        return testartifactList
    else:
        return None 
#------------------------------------------------------|

