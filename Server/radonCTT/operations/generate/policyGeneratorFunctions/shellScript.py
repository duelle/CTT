#==================================================================|
"""
>>>THIS IS A POLICY GENERATOR MODULE<<<
This module is responsible for generating PolicyTests for a given policy.
Related policies:
    - radon.policies.custom.ShellScript
"""
#==================================================================|
import json 

from swagger_server.models import PolicyTest

from radonCTT.database import databaseSession

#------------------------------------------------------|
def generatePolicyTest(project, testartifact, policy):
    """
    This is a >>>TERMINAL<<< generator function ->
    
    This is a policy generator function for the shellScript custom policy type.
    It creates a PolicyTest to represent the custom policy. It does not go any deeper in 
    the generator function layers.

    Args:
        - project (Project): The Project you wish to generate testartifacts for
        - testartifact (Testartifact): The Testartifact object to use for test generation
        - policy (Dict) : This policies representation in the servicetemplate
    """

    #Create the PolicyTest resource representing this performance policy
    policyTest = PolicyTest(
        status= project.status,
        project_id = project.id,
        testartifact_id= testartifact.id,    
        policy = json.dumps(policy)
    )
    databaseSession.add(policyTest)
    databaseSession.flush()
#------------------------------------------------------|

