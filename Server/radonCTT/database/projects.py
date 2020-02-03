#==================================================================|
"""
Contains helper methods to get Project objects from the database
"""
#==================================================================|

from swagger_server.models import Project

from radonCTT.database import databaseSession

#------------------------------------------------------|
def projectQueryToObject(projectQuery):
    """
    This helper method turns the response from the query
    into a propper Project object. This way, all the 
    swagger stuff is initialized on the object.
    """
    
    project =  Project (
        id=projectQuery.id,
        status=projectQuery.status,
        repository_url=projectQuery.repository_url,
        servicetemplate_location=projectQuery.servicetemplate_location,
        project_path=projectQuery.project_path,
    )

    project.query = projectQuery.query

    return project

#------------------------------------------------------|

#------------------------------------------------------|
def updateProject(project):
    """
    Updates a Project, but does not commit the changes
    """
    projectQuery = Project.query.get(project.id)
    
    projectQuery.status = project.status
    projectQuery.repository_url = project.repository_url
    projectQuery.servicetemplate_location = project.servicetemplate_location
    projectQuery.project_path = project.project_path

    databaseSession.flush()
#------------------------------------------------------|

#------------------------------------------------------|
def getProject(projectId: int):
    """
    Returns Project with given Id

    Args:
        projectId (int): Id of project to return
    """
    projectQuery = Project.query.get(projectId)

    if projectQuery:
        return projectQueryToObject(projectQuery)
    else:
        return None
#------------------------------------------------------|

#------------------------------------------------------|
def getProjects():
    """
    Returns all Projects in the database
    """

    projectQueries = Project.query.all()
    if projectQueries:   
        projectList = []
        for projectQuery in projectQueries:
            projectList.append(projectQueryToObject(projectQuery))
        return projectList
    else:
        return None 
#------------------------------------------------------|
