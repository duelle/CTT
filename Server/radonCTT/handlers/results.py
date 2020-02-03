#==================================================================|
"""
Contains all request handlers for result requests.
"""
#==================================================================|

import os
from flask import Response, send_file
import json
import shutil

from swagger_server.models.result import Result

from radonCTT.database import results as dbresults
from radonCTT.database.projects import getProject

#------------------------------------------------------|
def getResultById(resultId):
    """
    Returns a result for given ID

    Args:
        - resultId (int) : Id of result to return
    """

    if not isinstance(resultId, int):
        r = Response(response=f"Invalid Id: {resultId}", status='422',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    result = dbresults.getResult(resultId)

    if not result:
        r = Response(response= f"No result with Id: {resultId}", status='404',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    r = Response(response=json.dumps(result.to_dict()), status='200', mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|

#------------------------------------------------------|
def getResults():
    """
    Returns all results in the database
    """

    resultList = dbresults.getResults()

    if not resultList:
        r = Response(response='No results found', status='404', mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r
    
    r = Response(response=json.dumps(list(map(lambda model: model.to_dict(), resultList))), status='200',mimetype="text/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
#------------------------------------------------------|

#------------------------------------------------------|
def downloadResultById(resultId):
    """
    Sends the resultfile of a result back to the requester.

    Args:
        - resultId (int) : Id of result to download resultfile from
    """

    if not isinstance(resultId, int):
        r = Response(response= f"Invalid Id: {resultId}", status='422',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    result = dbresults.getResult(resultId)

    if not result:
        r = Response(response= f"No result with Id: {resultId}", status='404',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    project = getProject(result.project_id)

    if not project:
        r = Response(response=f"No project with Id: {result.project_id}", status='404',mimetype="text/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r

    zipTargetDir = f"{project.project_path}results"
    zipResultFile = f"{project.project_path}results.zip" 

    shutil.make_archive(zipTargetDir, 'zip', zipTargetDir)

    return send_file(zipResultFile, as_attachment=True, attachment_filename= "Results.zip")
#------------------------------------------------------|
