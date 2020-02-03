#==================================================================|
"""
Contains helper methods to get PolicyTest objects from the database
"""
#==================================================================|

from radonCTT.database.nodetests import getNodeTestsForPolicy

from swagger_server.models import PolicyTest

#------------------------------------------------------|
def policyTestQueryToObject(policyTestQuery):
    """
    This helper method turns the response from the query
    into a propper PolicyTest object. This way, all the 
    swagger stuff is initialized on the object.
    """

    return PolicyTest(
        id= policyTestQuery.id,
        status= policyTestQuery.status,
        project_id= policyTestQuery.project_id,
        testartifact_id= policyTestQuery.testartifact_id,
        policy= policyTestQuery.policy,
        node_tests= policyTestQuery.node_tests,
    )
#------------------------------------------------------|

#------------------------------------------------------|
def getPolicyTest(policyTestId, isLazyLoad):
    """
    Returns PolicyTest with given Id.

    Args:
        policyTestId (int) : Id of PolicyTest to load
        isLazyLoad (bool) : Wether or not to lazy load relations
    """

    policyTestQuery = PolicyTest.query.get(policyTestId)

    if isLazyLoad and policyTestQuery:
        policyTestQuery.node_tests = getNodeTestsForPolicy(policyTestQuery.id)

    if policyTestQuery:
        return policyTestQueryToObject(testartifactQuery)
    else:
        return None
#------------------------------------------------------|

#------------------------------------------------------|
def getPolicyTests():
    """
    Returns all PolicyTests in the database
    """

    policyTestsQuery = PolicyTest.query.all()
   
    if policyTestsQuery: 
        policyTestList = []
        for policyTestQuery in policyTestsQuery:
            policyTestList.append(policyTestQueryToObject(policyTestQuery))
        return policyTestList
    else:
        return None 
#------------------------------------------------------|

#------------------------------------------------------|
def getPolicyTestsForTestartifact(testartifactId):
    """
    Returns all PolicyTests in the database.
    PolicyTests are lazy-loaded.
    """

    policyTestsQuery = PolicyTest.query.filter_by(_testartifact_id=testartifactId)
    
    if policyTestsQuery: 
        policyTestList = []
        for policyTestQuery in policyTestsQuery:
            policyTestQuery.node_tests = getNodeTestsForPolicy(policyTestQuery.id)
            policyTestList.append(policyTestQueryToObject(policyTestQuery))
        return policyTestList
    else:
        return None 
#------------------------------------------------------|