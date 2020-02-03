#==================================================================|
"""
Contains all request handlers for project requests.

The Project can take four different states, based on which operations
have been performed on it:
    1. WAITING 
    2. TAGENERATED
    3. DEPLOYED
    4. EXECUTED
"""
#==================================================================|

import os
import json
import shutil

from flask import Response

from swagger_server.models.post_projects import POSTProjects
from swagger_server.models.project import Project
from swagger_server.models.testartifact import Testartifact
from swagger_server.models.policy_test import PolicyTest
from swagger_server.models.node_test import NodeTest
from swagger_server.models.deployment import Deployment
from swagger_server.models.executor import Executor
from swagger_server.models.result import Result

from radonCTT.database import databaseSession
from radonCTT.database import projects as dbprojects
from radonCTT.config import radonCTTConfig
from radonCTT.operations import importation

#------------------------------------------------------|
def createProject(postRequest : POSTProjects):
    """
    Handler function to create a new Project.

    Creates a new Project and initializes the project directory.
    It does this by cloning the repository specified in the request to the 
    general project directory specified in the radonCTTConfig
    """
    r = Response()
    
    if not postRequest.repository_url:
        r = Response(
            response='No repository url specified',
            status='422',
            mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    if not postRequest.servicetemplate_location:
        r = Response(
            response='No servicetemplate location specified',
            status='422',
            mimetype='text/xml')
        r.headers['Content-Type'] = 'text/xml; charset=utf-8'
        return r

    try:
        # --------------------------------------|
        # OBJECT CREATION   
        newProject = Project(
            status='WAITING',
            repository_url=postRequest.repository_url,
            servicetemplate_location=postRequest.servicetemplate_location,
            project_path='NaN')
        databaseSession.add(newProject)
        databaseSession.flush()

        # --------------------------------------|
        # IMPORT OPERATION
        importation.run(newProject)
        # --------------------------------------|

        r = Response(response= json.dumps(newProject.to_dict()),status='201',mimetype="text/json")
        r.headers["Content-Type"] = "application/json; charset=utf-8"

        databaseSession.commit()
    except:
        databaseSession.rollback()
        raise
    finally:
        databaseSession.remove()

    return r
#------------------------------------------------------|

#------------------------------------------------------|
def deleteProject(projectId):
    """
    Handler function to delete a Project
    """

    if not isinstance(projectId, int):
        r = Response(response='{}{}'.format('Invalid Id: ', projectId),status='422',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    try:
        # --------------------------------------|
        # GET/DELETE RELATED DATA

        projectQuery = Project.query.get(projectId)

        if not projectQuery:
            r = Response(response='{}{}'.format('No project with Id: ', projectId),status='404',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        # Get project directory before deleting
        projectDir = projectQuery.project_path
        databaseSession.delete(projectQuery)

        Testartifact.query.filter_by(_project_id=projectId).delete()
        PolicyTest.query.filter_by(_project_id=projectId).delete()
        NodeTest.query.filter_by(_project_id=projectId).delete()
        Deployment.query.filter_by(_project_id=projectId).delete()
        Executor.query.filter_by(_project_id=projectId).delete()
        Result.query.filter_by(_project_id=projectId).delete()

        # --------------------------------------|
        # ADDITIONAL LOGIC

        #Delete the project directory
        if os.path.exists(projectDir):
            shutil.rmtree(projectDir)

        # --------------------------------------|

        r = Response(response= '{}{}{}'.format('Project with Id: ', projectId, ' was deleted' ) ,status='201',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"

        databaseSession.commit()
    except:
        databaseSession.rollback()
        raise
    finally:
        databaseSession.remove()

    return r
#------------------------------------------------------|

#------------------------------------------------------|
def getProjectById(projectId):
    """
    Handler function to return a Project with given Id

    Args:
        -projectId (int) : Id of Project to return
    """

    if not isinstance(projectId, int):
        r = Response(
            response='{}{}'.format('Invalid Id: ', projectId),
            status='422',
            mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    project = dbprojects.getProject(projectId)

    if not project:
        r = Response(response='{}{}'.format('No project with Id: ', projectId),
            status='404',
            mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    r = Response(response= json.dumps(project.to_dict()), status='200',mimetype="text/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|
    
#------------------------------------------------------|
def getProjects():
    """
    Handler function to return all Projects
    """

    projectList = dbprojects.getProjects()

    if not projectList:
        r = Response(response='No projects found',status='404', mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r
    
    r = Response(response=json.dumps(list(map(lambda model: model.to_dict(), projectList))), status='200',mimetype="text/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|