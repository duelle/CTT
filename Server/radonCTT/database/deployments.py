#==================================================================|
"""
Contains helper methods to get Deployment objects from the database
"""
#==================================================================|

from swagger_server.models import Deployment

from radonCTT.database import databaseSession

#------------------------------------------------------|
def deploymentQueryToObject(deploymentQuery):
    """
    This helper method turns the response from the query
    into a propper Deployment object. This way, all the 
    swagger stuff is initialized on the object.
    """

    return Deployment(
        id=deploymentQuery.id,
        status=deploymentQuery.status,
        project_id=deploymentQuery.project_id,
        testartifact_id=deploymentQuery.testartifact_id,
    )
#------------------------------------------------------|

#------------------------------------------------------|
def updateDeployment(deployment : Deployment):
    """
    Updates a Deployment. However does not commit changes to the DB
    """

    deploymentQuery = Deployment.query.get(deployment.id)

    deploymentQuery.status = deployment.status
    deploymentQuery.project_id = deployment.project_id
    deploymentQuery.testartifact_id = deployment.testartifact_id

    databaseSession.flush()
#------------------------------------------------------|

#------------------------------------------------------|
def getDeployment(deploymentId):
    """
    Returns Deployment with given Id

    Args:
        deploymentId (int): Id of Deployment to return
    """

    deploymentQuery = Deployment.query.get(deploymentId)

    if deploymentQuery:
        return deploymentQueryToObject(deploymentQuery)
    else:
        return None
#------------------------------------------------------|

#------------------------------------------------------|
def getDeployments():
    """
    Returns all Deployments in the database
    """

    deploymentsQuery = Deployment.query.all()
    
    if deploymentsQuery:   
        deploymentList = []
        for deploymentQuery in deploymentsQuery:
            deploymentList.append(deploymentQueryToObject(deploymentQuery))
        return deploymentList
    else:
        return None 
#------------------------------------------------------|
