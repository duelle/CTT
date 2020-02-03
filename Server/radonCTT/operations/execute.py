#==================================================================|
"""
Contains the implementation of the export operation
"""
#==================================================================|
import os
import json
import subprocess

from swagger_server.models import Project, Deployment, Testartifact

#------------------------------------------------------|
def run(project : Project, deployment : Deployment, testartifact : Testartifact):
    """
    Runs the execute operation on every policy for a given project and deployment

    Args:
    - project (Project): The Project you wish to run the execute operation on
    - deployment (Deployment) : The Deployment you wish to execute
    - testartifact (Testartifact) : The Testartifact of the deployment
    """  

    # Map policy types to execution functions here
    functionSwitch = {
        # ##########################################################
        # POLICY TYPES ARE MAPPED TO POLICY EXECUTION FUNCTIONS HERE
        # ##########################################################

        # Custom : ShellScript
        'radon.policies.custom.ShellScript' : executeCustomShellScript 
    
    }

    for policyTest in testartifact.policy_tests:
        policy = json.loads(policyTest.policy)
        policyType = policy['type']

        if policyType in functionSwitch:
            executionFunction = functionSwitch[policyType]
            executionFunction(project, deployment, testartifact, policy)
#------------------------------------------------------|

#------------------------------------------------------|
def executeCustomShellScript(project : Project, deployment : Deployment, testartifact : Testartifact, policy):
    """
    Runs the execute operation for the shellScript policy type

    Args:
    - project (Project): The Project you wish to run the execute operation on
    - deployment (Deployment) : The Deployment you wish to execute
    - testartifact (Testartifact) : The Testartifact of the deployment
    - policy (Dict) : The policy represantation in the service template
    """  

    scriptPath = f"{policy['properties']['path']}"

    # Get into the project directory
    oldPath = os.getcwd()
    os.chdir(project.project_path)

    # Run the custom script
    subprocess.call(['bash', scriptPath])

    # Return to old working directory
    os.chdir(oldPath)
#------------------------------------------------------|

    