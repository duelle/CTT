#==================================================================|
"""
>>>THIS IS A NODE GENERATOR MODULE<<<
This module is responsible for generating NodeTests for a given node.
Related node:
    - radon.nodes.aws.LambdaFunction
"""
#==================================================================|

import os
import distutils.dir_util
import yaml
import json

from swagger_server.models.node_test import NodeTest

from radonCTT.database import databaseSession
from radonCTT.database.nodetests import updateNodeTest


#------------------------------------------------------|
def generateNodeTest(project, testartifact, policyTest, policy, node):
    """
    This is a node generator function for the lambdaFunction node type.
    It calls a node/policy generator function for the given policy type.

    Args:
        - project (Project): The Project you wish to generate this NodeTest for
        - testartifact (Testartifact): The Testartifact object to use for test generation
        - policyTest (PolicyTest) : The PolicyTest responsible for this NodeTest
        - policy (Dict) : The policy represantation in the servicetemplate
        - node (Dict) : This nodes represantation in the servicetemplate
    """

    #Define the node/policy generator function layer
    functionSwitch = {
        # ########################################################################
        # POLICY TYPES ARE MAPPED TO NODE SPECIFIC POLICY GENERATOR FUNCTIONS HERE
        # ########################################################################

        # AverageResponseTime 
        'radon.policies.performance.AverageResponseTime': generateTestForPolicyAverageResponseTime,

        # ResponseTimePercentile
        'radon.policies.performance.ResponseTimePercentile' : generateTestForPolicyAverageResponseTime,
    }

    if policy['type'] in functionSwitch:
        nodePolicyGeneratorFunction = functionSwitch[policy['type']]
        nodePolicyGeneratorFunction(project, testartifact, policyTest, policy, node)
#------------------------------------------------------| 

# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+
# AVERAGE RESPONSE TIME POLICY 
# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+

#------------------------------------------------------|
def generateTestForPolicyAverageResponseTime(project, testartifact, policyTest, policy, node):
    """
    This is a node/policy generator function for the lambdaFunction node type and the averageReponseTime policy.
    It calls a node/policy/runner generator function for the chosen runner type.

    Args:
        - project (Project): The Project you wish to generate this NodeTest for
        - testartifact (Testartifact): The Testartifact object to use for test generation
        - policyTest (PolicyTest) : The PolicyTest responsible for this NodeTest
        - policy (Dict) : The policy represantation in the servicetemplate
        - node (Dict) : This nodes represantation in the servicetemplate
    """

    #Define the node/policy/runner generator function layer
    functionSwitch = {
        # Python
        'python': generateTestForPolicyAverageResponseTimeRunnerPython,
    }

    if policy['properties']['runner'] in functionSwitch:
        nodePolicyRunnerGeneratorFunction = functionSwitch[policy['properties']['runner']]
        nodePolicyRunnerGeneratorFunction(project, testartifact, policyTest, policy, node)
#------------------------------------------------------|

#------------------------------------------------------|
def generateTestForPolicyAverageResponseTimeRunnerPython(project, testartifact, policyTest, policy, node):
    """
    This is a node/policy/runner generator function for the lambdaFunction node type and the averageReponseTime policy and the python runner.
    The LambdaFunction has one more property which we need to go one more generator layer deep, the event property.

    Args:
        - project (Project): The Project you wish to generate this NodeTest for
        - testartifact (Testartifact): The Testartifact object to use for test generation
        - policyTest (PolicyTest) : The PolicyTest responsible for this NodeTest
        - policy (Dict) : The policy represantation in the servicetemplate
        - node (Dict) : This nodes represantation in the servicetemplate
    """

    #Define the node/policy/runner/event generator function layer
    functionSwitch = {
        # Object created in S3 Bucket
        's3:ObjectCreated:*': generateTestForPolicyAverageResponseTimeRunnerPythonEventObjectCreated,
    }

    #TODO: Future Work : 
    # Currently, we just call the Generator-Function for 's3:ObjectCreated:' event.
    # In the future, we would actually look at which node is triggering our 
    # lambda-function and call a function based on how the trigger happens.

    nodePolicyRunnerEventGeneratorFunction = functionSwitch['s3:ObjectCreated:*']
    nodePolicyRunnerEventGeneratorFunction(project, testartifact, policyTest, policy, node)
#------------------------------------------------------|

#------------------------------------------------------|
def generateTestForPolicyAverageResponseTimeRunnerPythonEventObjectCreated(project, testartifact, policyTest, policy, node):
    """
    This is a >>>TERMINAL<<< generator function for the lambdaFunction node type 
    and the averageReponseTime policy and the python runner and the object created event.
    It copies the related template and fills it with parameters from the policy and node.

    Args:
        - project (Project): The Project you wish to generate this NodeTest for
        - testartifact (Testartifact): The Testartifact object to use for test generation
        - policyTest (PolicyTest) : The PolicyTest responsible for this NodeTest
        - policy (Dict) : The policy represantation in the servicetemplate
        - node (Dict) : This nodes represantation in the servicetemplate
    """
    #Create a NodeTest to represent this node
    nodeTest = NodeTest(
        status= project.status,
        project_id= project.id,
        policy_test_id= policyTest.id,
        node = json.dumps(node),
        artifact_path= '',
    )
    databaseSession.add(nodeTest)
    databaseSession.flush()

    #Set the path this NodeTests artifacts will be placed in
    nodeTest.artifact_path = f"{project.project_path}testartifacts{os.path.sep}{policyTest.id}{os.path.sep}{nodeTest.id}{os.path.sep}"
    updateNodeTest(nodeTest)

    # Generate the NodeTests artifact directory
    directory = os.path.dirname(nodeTest.artifact_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


    #Get the template parameters from the policy and node
    # +++TEMPLATE PARAMETERS+++
    # ARG 1 : REPEATS
    # ARG 2 : FUNCTION_NAME
    # ARG 3 : SOURCE_FILE_PREFIX
    # ARG 4 : SOURCE_FILE_POSTFIX
    # ARG 5 : BUCKET_NAME
    # ARG 6 : SOURCE_FILE_PATH
    # ARG 7 : RESULT_PATH
    # ARG 8 : UNIQUE_TEST_ID
    # +++++++++++++++++++++++++

    repeats = f"{policy['properties']['repeats']}"
    function_name = f"{node['properties']['function_name']}"
    source_file_prefix = f"{node['properties']['trigger_file_prefix']}"
    source_file_postfix = f"{node['properties']['trigger_file_postfix']}"
    bucket_name = f"{node['properties']['trigger_bucket_name']}"
    source_file_path = f"{project.project_path}{source_file_prefix}{source_file_postfix}"
    result_path = f"{nodeTest.artifact_path}"
    unique_test_id = f"{nodeTest.id}"

    # We need the absolute path to the template
    templatePath = f"{os.getcwd()}{os.path.sep}radonCTT{os.path.sep}templates{os.path.sep}averageResponseTime{os.path.sep}aws{os.path.sep}lambdaFunction{os.path.sep}python-object-create{os.path.sep}"

    # Copy the template into our NodeTest artifact directory
    distutils.dir_util.copy_tree(templatePath, nodeTest.artifact_path)

    # Fill the absolute path to the python runner into the python playbook and call with our arguments
    playbookPath = f"{nodeTest.artifact_path}artifacts{os.path.sep}create.yml"
    pythonRunnerPath = f"{nodeTest.artifact_path}artifacts{os.path.sep}run.py"
    pythonRunCommand = f"{pythonRunnerPath} {repeats} {function_name} {source_file_prefix} {source_file_postfix} {bucket_name} {source_file_path} {result_path} {unique_test_id}"

    # Read and edit
    with open(playbookPath) as instream:
        try:
            playbook = yaml.safe_load(instream)
            playbook[0]['tasks'][0]['script'] = pythonRunCommand
        except yaml.YAMLError as exc:
            print(exc)
    
    # Push edits
    with open(playbookPath, "w") as outstream:
        try:
            yaml.dump(playbook, outstream)
        except yaml.YAMLError as exc:
            print(exc)
#------------------------------------------------------|
# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+
