#==================================================================|
"""
Contains helper methods to get Deployment objects from the database
"""
#==================================================================|

from swagger_server.models import Executor

#------------------------------------------------------|
def executorQueryToObject(executorQuery):
    """
    This helper method turns the response from the query
    into a propper Executor object. This way, all the 
    swagger stuff is initialized on the object.
    """

    return Executor(
        id=executorQuery.id,
        status=executorQuery.status,
        project_id= executorQuery.project_id,
        deployment_id=executorQuery.deployment_id,
    )
#------------------------------------------------------|

#------------------------------------------------------|
def getExecutor(executorId):
    """
    Returns Executor with given Id

    Args:
        executorId (int): Id of Executor to return
    """

    executorQuery = Executor.query.get(executorId)

    if executorQuery:
       return executorQueryToObject(executorQuery)
    else:
        return None
#------------------------------------------------------|

#------------------------------------------------------|
def getExecutors():
    """
    Returns all Executors in the database
    """

    executorsQuery = Executor.query.all()

    if executorsQuery:   
        executorList = []
        for executorQuery in executorsQuery:
            executorList.append(executorQueryToObject(executorQuery))
        return executorList
    else:
        return None 
#------------------------------------------------------|
