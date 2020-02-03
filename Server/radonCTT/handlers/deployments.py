#==================================================================|
"""
Contains all request handlers for deployment requests.
"""
#==================================================================|

from flask import Response

import json
import os
import subprocess
import time 

from swagger_server.models.post_deployments import POSTDeployments
from swagger_server.models.deployment import Deployment
from swagger_server.models.testartifact import Testartifact
from swagger_server.models.project import Project

from radonCTT.database import databaseSession
from radonCTT.database.projects import getProject, updateProject
from radonCTT.database.testartifacts import getTestartifact, updateTestartifact
from radonCTT.database import deployments as dbdeployments
from radonCTT.operations import deploy


#------------------------------------------------------|
def createDeployment(postRequest : POSTDeployments):
    r = Response()

    try:
        # --------------------------------------|
        # GET/UPDATE RELATED DATA
        if not isinstance(postRequest.testartifact_id, int):
            r = Response(response='{}{}'.format('Invalid Id: ', postRequest.testartifact_id), status='422',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        testartifact = getTestartifact(postRequest.testartifact_id, True)

        if not testartifact:
            r = Response(response='{}{}'.format('No testartifact with Id: ', postRequest.testartifact_id), status='404',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        project = getProject(testartifact.project_id)

        if not project:
            r = Response(response='{}{}'.format('No project with Id: ', testartifact.project_id), status='404',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        testartifact.status = 'DEPLOYED'
        project.status = 'DEPLOYED'

        updateTestartifact(testartifact)
        updateProject(project)

        # --------------------------------------|
        # OBJECT CREATION
        deployment = Deployment(
            status= 'DEPLOYED',
            project_id= project.id,
            testartifact_id= testartifact.id,
        )

        databaseSession.add(deployment)
        databaseSession.flush()
        # --------------------------------------|
        # DEPLOY OPERATION
        deploy.run(project, testartifact)
        # --------------------------------------|

        r = Response(response=json.dumps(deployment.to_dict()),status='201',mimetype="application/json")
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
def getDeploymentById(deploymentId):
    if not isinstance(deploymentId, int):
        r = Response(response='{}{}'.format('Invalid Id: ', deploymentId), status='422',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    deployment = dbdeployments.getDeployment(deploymentId)

    if not deployment:
        r = Response(response='{}{}'.format('No deployment with Id: ', deploymentId), status='404',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    r = Response(response=json.dumps(deployment.to_dict()), status='200', mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|

#------------------------------------------------------|
def getDeployments():
    deploymentList = dbdeployments.getDeployments()

    if not deploymentList:
        r = Response(response='No deployments found', status='404', mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r
    
    r = Response(response=json.dumps(list(map(lambda model: model.to_dict(), deploymentList))), status='200',mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|