#==================================================================|
"""
Contains the implementation of the deploy operation
"""
#==================================================================|

import os
import time
import subprocess

from swagger_server.models.project import Project
from swagger_server.models.testartifact import Testartifact

#------------------------------------------------------|
def run(project : Project, testartifact : Testartifact):
    """
    Runs the deploy operation on the given Project

    Args:
    - project (Project): The Project you wish to run the deploy operation on
    - testartifact (Testartifact) : The testartifact to deploy
    """


    #+#+#+#+#+#+#+#+|
    # SUT DEPLOYMENT|
    #+#+#+#+#+#+#+#+|

    # Get into the project directory
    oldPath = os.getcwd()
    os.chdir(project.project_path)

    # Run the deployment-script if it's present
    if os.path.isfile('radon-ctt/deployment.sh'):
        subprocess.call(['bash', 'radon-ctt/deployment.sh'])

    # Deploy the servicetemplate with opera
    subprocess.call(['opera','deploy', f"DEPLOYMENT_PROJECT_{project.id}", f"{project.servicetemplate_location}"])

    os.chdir(oldPath)

    #>>>!!!<<<
    # WAIT 10 S BETWEEN SUT AND TA DEPLOYMENT
    time.sleep(10)
    #>>>!!!<<<

    #+#+#+#+#+#+#+#+|
    # TA DEPLOYMENT |
    #+#+#+#+#+#+#+#+|
    for policyTest in testartifact.policy_tests:
        for nodeTest in policyTest.node_tests:
            os.chdir(nodeTest.artifact_path)
            subprocess.call(['opera','deploy', f"DEPLOYMENT_PROJECT_{project.id}_TA_{nodeTest.id}", 'servicetemplate.yml'])

    os.chdir(oldPath)
#------------------------------------------------------|

    
