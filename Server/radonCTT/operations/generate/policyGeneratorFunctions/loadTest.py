#==================================================================|
"""
>>>THIS IS A POLICY GENERATOR MODULE<<<
This module is responsible for generating PolicyTests for a given policy.
Related policies:
    - radon.policies.performance.LoadTest
"""
#==================================================================|
import os
import json 

from swagger_server.models import PolicyTest


from radonCTT import parser

from radonCTT.database import databaseSession

from radonCTT.operations.generate.nodeGeneratorFunctions import webApplication

#------------------------------------------------------|
def generatePolicyTest(project, testartifact, policy):
    """
    This is a policy generator function for the loadTest performance policy type.
    It creates a PolicyTest to represent the performance policy and then calls node generator
    functions.

    Args:
        - project (Project): The Project you wish to generate testartifacts for
        - testartifact (Testartifact): The Testartifact object to use for test generation
        - policy (Dict) : This policies representation in the servicetemplate
    """

    # Define the node generator function layer
    functionSwitch = {
        # #################################################################
        # NODE TYPES ARE MAPPED TO NODE GENERATOR FUNCTIONS HERE
        # #################################################################

        # WebApplication
        'radon.nodes.docker.WebApplication' : webApplication.generateNodeTest
    }

    #Create the PolicyTest resource representing this performance policy
    policyTest = PolicyTest(
        status= project.status,
        project_id = project.id,
        testartifact_id= testartifact.id,    
        policy = json.dumps(policy)
    )
    databaseSession.add(policyTest)
    databaseSession.flush()

    #Generate a directory for the PolicyTest
    directory = os.path.dirname(f"{project.project_path}testartifacts{os.path.sep}{policyTest.id}{os.path.sep}")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Call a node generator function for every node targeted by this performance policy
    for nodeName in parser.getNodeTemplates():
        node = parser.getNodeTemplates().get(nodeName)
        if (node['type'] in functionSwitch) and (nodeName in policy['targets'][0]):
            nodeGeneratorFunc = functionSwitch[node['type']]
            nodeGeneratorFunc(project, testartifact, policyTest, policy, node)
#------------------------------------------------------|

