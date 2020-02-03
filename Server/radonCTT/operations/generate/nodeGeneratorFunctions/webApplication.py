#==================================================================|
"""
>>>THIS IS A NODE GENERATOR MODULE<<<
This module is responsible for generating NodeTests for a given node.
Related node:
    - radon.nodes.docker.WebApplication
"""
#==================================================================|

import os
import distutils.dir_util
import yaml
import json
import xml.etree.ElementTree as ET
import copy

from swagger_server.models.node_test import NodeTest

from radonCTT.database import databaseSession
from radonCTT.database.nodetests import updateNodeTest


#------------------------------------------------------|
def generateNodeTest(project, testartifact, policyTest, policy, node):
    """
    This is a node generator function for the WebApplication node type.
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

        # LoadTest
        'radon.policies.performance.LoadTest': generateTestForPolicyLoadTest,
    }

    if policy['type'] in functionSwitch:
        nodePolicyGeneratorFunction = functionSwitch[policy['type']]
        nodePolicyGeneratorFunction(project, testartifact, policyTest, policy, node)
#------------------------------------------------------| 

# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+
# LOAD TEST POLICY 
# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+

#------------------------------------------------------|
def generateTestForPolicyLoadTest(project, testartifact, policyTest, policy, node):
    """
    This is a node/policy generator function for the WebApplication node type and the loadTest policy.
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
        # JMETER
        'jmeter': generateTestForPolicyLoadTestRunnerJmeter,
    }

    if policy['properties']['runner'] in functionSwitch:
        nodePolicyRunnerGeneratorFunction = functionSwitch[policy['properties']['runner']]
        nodePolicyRunnerGeneratorFunction(project, testartifact, policyTest, policy, node)
#------------------------------------------------------|

#------------------------------------------------------|
def generateTestForPolicyLoadTestRunnerJmeter(project, testartifact, policyTest, policy, node):
    """
    This is a >>>TERMINAL<<< generator function for the WebApplication node type and the loadTest policy and the jmeter runner.

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


    #Get information from the policy and node to create the testplan from a template
    # +++TEMPLATE PARAMETERS+++
    # 1 : THREADS
    # 2 : REPEATS
    # 3 : UPPER_BOUND
    # 4 : HOST
    # 5 : PORTS
    # +++++++++++++++++++++++++

    threads = f"{policy['properties']['threads']}"
    repeats = f"{policy['properties']['repeats']}"
    upper_bound = f"{policy['properties']['upper_bound']}"
    host = f"{node['properties']['host']}"
    ports = node.get('properties').get('ports')

    # We need the absolute path to the testplan template to copy it
    templatePath = f"{os.getcwd()}{os.path.sep}radonCTT{os.path.sep}templates{os.path.sep}loadTest{os.path.sep}webApplication{os.path.sep}jmeter-load-test{os.path.sep}"

    # Copy the testplan template into our NodeTest artifact directory
    distutils.dir_util.copy_tree(templatePath, nodeTest.artifact_path)

    # Fill the absolute path to the testplan into the playbook and call with our arguments
    playbookPath = f"{nodeTest.artifact_path}artifacts{os.path.sep}create.yml"
    testplanPath = f"{nodeTest.artifact_path}artifacts{os.path.sep}testplan.jmx"
    jmeterRunCommand = f"jmeter -n -t {testplanPath} -l {nodeTest.artifact_path}result.csv"

    # <<<<<<<<<<<<<<<<< PLAY BOOK EDITING >>>>>>>>>>>>>>>>>

    # Read and edit
    with open(playbookPath) as instream:
        try:
            playbook = yaml.safe_load(instream)
            playbook[0]['tasks'][0]['shell'] = jmeterRunCommand
        except yaml.YAMLError as exc:
            print(exc)
    
    # Push edits
    with open(playbookPath, "w") as outstream:
        try:
            yaml.dump(playbook, outstream)
        except yaml.YAMLError as exc:
            print(exc)

    # <<<<<<<<<<<<<<<<< TEST PLAN EDITING >>>>>>>>>>>>>>>>>
    tree = ET.parse(testplanPath)
    root = tree.getroot()

    # Write metadata to the testplan
    threadGroupHashTree = root[0][1]
    threadGroup = threadGroupHashTree[0]
    threadGroupController = threadGroup[1]
    subThreadGroupHashTree = threadGroupHashTree[1]


    durationAssertion = subThreadGroupHashTree[0]
    subThreadGroupHashTreeSeparator = subThreadGroupHashTree[1]
    httpSampler = subThreadGroupHashTree[2]

    # DURATION
    durationAssertionDuration = durationAssertion[0]
    durationAssertionDuration.text = upper_bound

    # LOOPS
    loopController = threadGroupController[1]
    loopController.text = repeats

    # THREADS
    threadGroupNumThreads = threadGroup[2]
    threadGroupNumThreads.text = threads

    # Create Samplers for every pathill NodeTestAverages into the list
    isFirstHttpSampler = True
    for port in ports:
        paths = ports.get(port)
        for path in paths:
            if isFirstHttpSampler:
                newHttpSampler = httpSampler
            else:
                newHttpSampler = copy.deepcopy(httpSampler)

            newSeparator = copy.deepcopy(subThreadGroupHashTreeSeparator)

            #Set the values in the HTTP Sampler
            httpSamplerHost = newHttpSampler[1]
            httpSamplerPort = newHttpSampler[2]
            httpSamplerPath = newHttpSampler[7]

            httpSamplerHost.text = f"{host}"
            httpSamplerPort.text = f"{port}"
            httpSamplerPath.text = f"{path}"

            if isFirstHttpSampler:
                isFirstHttpSampler = False 
            else:
                subThreadGroupHashTree.append(newHttpSampler)
                subThreadGroupHashTree.append(newSeparator)
                
    #Write the changes to the file
    tree.write(testplanPath)
    # <<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>
#------------------------------------------------------|
# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+
