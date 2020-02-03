#==================================================================|
"""
Contains the implementation of the import operation
"""
#==================================================================|

import os

from git import Repo

from swagger_server.models.project import Project

from radonCTT.config import radonCTTConfig

from radonCTT.database import databaseSession

#------------------------------------------------------|
def run(project : Project):
    """
    Runs the import operation on the given Project

    Args:
    - project (Project): The Project you wish to run the import operation on
    """

    #Get the project path
    projectPath = f"{radonCTTConfig['PATHS']['Project_Dir']}{project.id}{os.path.sep}"

    
    #Create the directory for the new project
    directory = os.path.dirname(projectPath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Copy the SUT into it
    repo = Repo.clone_from(project.repository_url, projectPath)

    #Save Project path in Project resource
    project.project_path = projectPath
    databaseSession.flush()
#------------------------------------------------------|
