#==================================================================|
"""
Contains all request handlers for testartifact requests
"""
#==================================================================|

import os
import json
import shutil

from flask import Response, send_file

from swagger_server.models.post_testartifacts import POSTTestartifacts
from swagger_server.models.testartifact import Testartifact
from swagger_server.models.project import Project

from radonCTT.database import databaseSession
from radonCTT.database import testartifacts as dbtestartifacts
from radonCTT.database.projects import getProject, updateProject

from radonCTT.operations import generate

#------------------------------------------------------|
def createTestartifact(postRequest : POSTTestartifacts):
    """
    Creates Testartifacts for a Project
    """
    r = Response()

    try:
        # --------------------------------------|
        # GET/UPDATE RELATED DATA
        if not isinstance(postRequest.project_id, int):
            r = Response(response=f"Invalid Id: {postRequest.project_id}", status='422',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        project = getProject(postRequest.project_id)

        if not project:
            r = Response(response=f"No project with Id: {postRequest.project_id}", status='404',mimetype="text/xml")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return r

        project.status = 'TAGENERATED'

        updateProject(project)

        # --------------------------------------|
        # OBJECT CREATION
        testartifact = Testartifact(
            status= project.status,
            project_id= project.id,
        )
        databaseSession.add(testartifact)
        databaseSession.flush()
        # --------------------------------------|
        # GENERATE OPERATION
        generate.run(project, testartifact)
        # --------------------------------------|

        newTestartifact = dbtestartifacts.getTestartifactForProject(project, True)

        r = Response(response=json.dumps(newTestartifact.to_dict()),status='201',mimetype="application/json")
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
def getTestArtifactById(testartifactId):
    if not isinstance(testartifactId, int):
        r = Response(response=f"Invalid Id: {testartifactId}", status='422',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    testartifact = dbtestartifacts.getTestartifact(testartifactId, False)

    if not testartifact:
        r = Response(response=f"No testartifact with Id: {testartifactId}", status='404',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    r = Response(response=json.dumps(testartifact.to_dict()), status='200', mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|

#------------------------------------------------------|
def getTestArtifacts():
    testartifactList = dbtestartifacts.getTestartifacts()

    if not testartifactList:
        r = Response(response='No testartifacts found', status='404', mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r
    
    r = Response(response=json.dumps(list(map(lambda model: model.to_dict(), testartifactList))), status='200',mimetype="text/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|

#------------------------------------------------------|
def downloadTestartifactById(testartifactId):
    if not isinstance(testartifactId, int):
        r = Response(response=f"Invalid Id: {testartifactId}", status='422',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    testartifact = dbtestartifacts.getTestartifact(testartifactId, False)

    if not testartifact:
        r = Response(response=f"No testartifact with Id: {testartifactId}", status='404',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    project = getProject(testartifact.project_id)

    if not project:
        r = Response(response=f"No project with Id: {testartifact.project_id}", status='404',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    zipFilePath = f"{project.project_path}Artifact"

    shutil.make_archive(zipFilePath, 'zip', f"{project.project_path}testartifacts{os.path.sep}")

    return send_file(f"{zipFilePath}.zip", as_attachment=True, attachment_filename='Artifact.zip')
#------------------------------------------------------|

