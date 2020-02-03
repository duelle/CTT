#==================================================================|
"""
Contains all request handlers for executor requests.
"""
#==================================================================|


import json
import os
import csv

from flask import Response
from shutil import copyfile

from swagger_server.models import POSTExecutors, Result, Executor, Deployment, Testartifact, Project


from radonCTT.config import radonCTTConfig

from radonCTT.database import databaseSession
from radonCTT.database import executors as dbexecutors
from radonCTT.database.projects import getProject, updateProject
from radonCTT.database.testartifacts import getTestartifact, updateTestartifact
from radonCTT.database.deployments import getDeployment, updateDeployment

from radonCTT.operations import execute, evaluate

#------------------------------------------------------|
def createExecutor(postRequest : POSTExecutors):
    r = Response()
    
    try:
        # --------------------------------------|
        # GET/UPDATE RELATED DATA
        if not isinstance(postRequest.deployment_id, int):
            r = Response(response='{}{}'.format('Invalid Id: ', postRequest.deployment_id), status='422',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        deployment = getDeployment(postRequest.deployment_id)

        if not deployment:
            r = Response(response='{}{}'.format('No deployment with Id: ', postRequest.deployment_id), status='404',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        testartifact = getTestartifact(deployment.testartifact_id, True)

        if not testartifact:
            r = Response(response='{}{}'.format('No testartifact with Id: ', deployment.testartifact_id), status='404',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        project = getProject(deployment.project_id)

        if not project:
            r = Response(response='{}{}'.format('No project with Id: ', deployment.project_id), status='404',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        project.status = 'EXECUTED'
        testartifact.status = 'EXECUTED'
        deployment.status = 'EXECUTED'
        
        updateProject(project)
        updateTestartifact(testartifact)
        updateDeployment(deployment)

        # --------------------------------------|
        # OBJECT CREATION
        executor = Executor(
            status='EXECUTED',
            project_id=project.id,
            deployment_id=deployment.id,
        )
        databaseSession.add(executor)
        databaseSession.flush()

        result = Result(
            project_id=project.id,
            testartifact_id=testartifact.id,
            result_path=f"{project.project_path}results{os.path.sep}report.csv",
        )
        databaseSession.add(result)
        databaseSession.flush()
        # --------------------------------------|
        # EXECUTE OPERATION
        execute.run(project, deployment, testartifact)
        # --------------------------------------|
        # EVALUATE OPERATION
        evaluate.run(project, testartifact, result)
        # --------------------------------------|

        r = Response(response=json.dumps(result.to_dict()),status='201',mimetype="application/json")
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
def getExecutorById(executorId):
    if not isinstance(executorId, int):
        r = Response(response='{}{}'.format('Invalid Id: ', executorId), status='422',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    executor = dbexecutors.getExecutor(executorId)

    if not executor:
        r = Response(response='{}{}'.format('No executor with Id: ', executorId), status='404',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    r = Response(response=json.dumps(executor.to_dict()), status='200', mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|

#------------------------------------------------------|
def getExecutors():
    executorList = dbexecutors.getExecutors()

    if not executorList:
        r = Response(response='No executors found', status='404', mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r
    
    r = Response(response=json.dumps(list(map(lambda model: model.to_dict(), executorList))), status='200',mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|