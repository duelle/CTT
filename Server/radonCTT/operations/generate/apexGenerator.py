#==================================================================|
"""
Contains the implementation of the generate operation
"""
#==================================================================|
import os

from swagger_server.models import Project, Testartifact

from radonCTT import parser
from radonCTT.operations.generate.policyGeneratorFunctions import averageResponseTime, loadTest, shellScript

#------------------------------------------------------|
def run(project : Project, testartifact : Testartifact):
    """
    Runs the generate operation on the given Project using the given Testartifact

    Args:
    - project (Project): The Project you wish to run the generate operation on
    - testartifact (Testartifact) : The Testartifact to use for the generate operation
    """
    
    #Parse the target SUT service template
    parser.parse(f"{project.project_path}{project.servicetemplate_location}")

    # Define the policy generator function layer
    functionSwitch = {
        # ##########################################################
        # POLICY TYPES ARE MAPPED TO POLICY GENERATOR FUNCTIONS HERE
        # ##########################################################

        # AverageResponseTime
        'radon.policies.performance.AverageResponseTime': averageResponseTime.generatePolicyTest,

        # ResponseTimePercentile
        'radon.policies.performance.ResponseTimePercentile': averageResponseTime.generatePolicyTest,

        # LoadTest
        'radon.policies.performance.LoadTest': loadTest.generatePolicyTest,

        # Custom : ShellScript
        'radon.policies.custom.ShellScript' : shellScript.generatePolicyTest,
    
    }

    #Make a directory for the Testartifact
    directory = os.path.dirname(f"{project.project_path}testartifacts{os.path.sep}")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Call a policy generator function for every policy in the service template
    for policyName in parser.getPolicies():
        policy = parser.getPolicies().get(policyName)
        if policy['type'] in functionSwitch:
            policyGeneratorFunc = functionSwitch[policy['type']]
            policyGeneratorFunc(project, testartifact, policy)
#------------------------------------------------------|