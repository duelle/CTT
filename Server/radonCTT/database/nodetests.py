#==================================================================|
"""
Contains helper methods to get NodeTest objects from the database
"""
#==================================================================|

from swagger_server.models import NodeTest

from radonCTT.database import databaseSession

#------------------------------------------------------|
def nodeTestQueryToObject(nodeTestQuery):
    """
    This helper method turns the response from the query
    into a propper Project object. This way, all the 
    swagger stuff is initialized on the object.
    """
    
    return NodeTest(
        id = nodeTestQuery.id,
        status= nodeTestQuery.status,
        project_id= nodeTestQuery.project_id,
        policy_test_id= nodeTestQuery.policy_test_id,
        node= nodeTestQuery.node,
        artifact_path= nodeTestQuery.artifact_path,
    )
#------------------------------------------------------|

#------------------------------------------------------|
def updateNodeTest(nodeTest : NodeTest):
    """
    Updates a nodeTest, but does not commit the changes.
    """

    nodeTestQuery = NodeTest.query.get(nodeTest.id)
    nodeTestQuery.status = nodeTest.status
    nodeTestQuery.project_id = nodeTest.project_id
    nodeTestQuery.policy_test_id = nodeTest.policy_test_id
    nodeTestQuery.node = nodeTest.node
    nodeTestQuery.artifact_path = nodeTest.artifact_path

    databaseSession.flush()
#------------------------------------------------------|


#------------------------------------------------------|
def getNodeTest(nodeTestId: int):
    """
    Returns NodeTest with given Id

    Args:
        nodeTestId (int): Id of NodeTest to return
    """

    nodeTestQuery = NodeTest.query.get(nodeTestId)

    if nodeTestQuery:
        return nodeTestQueryToObject(nodeTestQuery)
    else:
        return None
#------------------------------------------------------|

#------------------------------------------------------|
def getNodeTests():
    """
    Returns all NodeTests in the database
    """

    nodeTestsQuery = NodeTest.query.all()
    
    if nodeTestsQuery:   
        nodeTestList = []
        for nodeTestQuery in nodeTestsQuery:
            nodeTestList.append(nodeTestQueryToObject(nodeTestQuery))
        return nodeTestList
    else:
        return None 
#------------------------------------------------------|

#------------------------------------------------------|
def getNodeTestsForPolicy(policyTestId):
    """
    Returns all NodeTests in the database related to the policyTest

    Args:
        policyId (int) : policyTest to get related nodetests from
    """

    nodeTestsQuery = NodeTest.query.filter_by(_policy_test_id=policyTestId)
    
    if nodeTestsQuery:   
        nodeTestList = []
        for nodeTestQuery in nodeTestsQuery:
            nodeTestList.append(nodeTestQueryToObject(nodeTestQuery))
        return nodeTestList
    else:
        return None 
#------------------------------------------------------|
