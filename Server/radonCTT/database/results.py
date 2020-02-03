#==================================================================|
"""
Contains helper methods to get Deployment objects from the database
"""
#==================================================================|

from swagger_server.models import Result

#------------------------------------------------------|
def resultQueryToObject(resultQuery):
    """
    This helper method turns the response from the query
    into a propper Result object. This way, all the 
    swagger stuff is initialized on the object.
    """
    
    return Result(
        id=resultQuery.id,
        project_id=resultQuery.project_id,
        testartifact_id=resultQuery.testartifact_id,
        result_path=resultQuery.result_path,
    )
#------------------------------------------------------|

#------------------------------------------------------|
def getResult(resultId):
    """
    Returns Result with given Id

    Args:
        resultId (int): Id of Result to return
    """

    resultQuery = Result.query.get(resultId)

    if resultQuery:
        return resultQueryToObject(resultQuery)
    else:
        return None
#------------------------------------------------------|

#------------------------------------------------------|
def getResults():
    """
    Returns all Results in the database
    """

    resultQueries = Result.query.all()
    
    if resultQueries:   
        resultList = []
        for resultQuery in resultQueries:
            resultList.append(resultQueryToObject(resultQuery))
        return resultList
    else:
        return None 
#------------------------------------------------------|