#==================================================================|
"""
Contains the implementation of the evaluate operation
"""
#==================================================================|
import os
import shutil
import json
import csv
from statistics import mean
import numpy

from swagger_server.models import PolicyTest, Project, Testartifact, Result

from radonCTT.database import databaseSession

#------------------------------------------------------|
def run(project : Project, testartifact : Testartifact, result : Result):
    """
    Runs the evaluate operation on the given Project and Testartifact

    Args:
    - project (Project): The Project you wish to run the evaluate operation on
    - testartifact (Testartifact) : The Testartifact you wish to evaluate
    """      
    #Create a directory for the evaluation report  
    directory = os.path.dirname(f"{project.project_path}results{os.path.sep}")
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(result.result_path, 'w') as result_file:
        writer = csv.writer(result_file, delimiter = ';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Every PolicyTest is entered individually into the result file
        for policyTest in testartifact.policy_tests:
            evaluatePolicyTest(policyTest, writer, project)
#------------------------------------------------------|



#------------------------------------------------------|
def evaluatePolicyTest(policyTest : PolicyTest, writer, project : Project):
    """
    Evaluates a policytest and writes the results with a writer.

    Args:
        - policyTest (PolicyTest) : The policyTest object to create results for
        - writer (csv_writer) : A writer to write the results
    """
    #Definethe policy evaluate function layer
    functionSwitch = {
        # #################################################################
        # POLICY TYPES ARE MAPPED TO RESULT FUNCTIONS HERE
        # #################################################################

        # AverageResponseTime
        'radon.policies.performance.AverageResponseTime' : evaluateAverageResponseTime,

        # ResponseTimePercentile
        'radon.policies.performance.ResponseTimePercentile' : evaluateResponseTimePercentile,

        # LoadTest
        'radon.policies.performance.LoadTest' : evaluateLoadTest,
    }

    policy = json.loads(policyTest.policy)
    policyType = policy['type']

    if policyType in functionSwitch:
        evaluationFunction = functionSwitch[policyType]
        evaluationFunction(policyTest, policy, writer, project)
#------------------------------------------------------|

#------------------------------------------------------|
def evaluateAverageResponseTime(policyTest : PolicyTest, policy, writer , project : Project):
    """
    Generates and writes results for PolicyTest of type AverageResponseTime into the result file

    Args:
        - policyTest (PolicyTest) : The policyTest object to create results for
        - policy (dict) : The yaml represantation of the policy
        - writer (csv_writer) : A writer to write the results
    """
    nodeTestResults = []

    upper_bound = float(policy.get('properties')['upper_bound'])
    lower_bound = float(policy.get('properties')['lower_bound'])
    repeats = float(policy.get('properties')['repeats'])
    fuse = bool(policy.get('properties')['fuse'])

    # Fill NodeTestAverages into the list
    for nodeTest in policyTest.node_tests:
        node = json.loads(nodeTest.node)
        nodeType = node['type']

        resultPath = f"{nodeTest.artifact_path}results.csv"
        
        resultList = []
        # Get the results from the csv
        with open(resultPath, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                resultList.append(float(row[0]))

        nodeTestEntry = {
            'type' : nodeType,
            'result' : mean(resultList),
        }

        nodeTestResults.append(nodeTestEntry)

    # Create the policyTest entry into the result
    if fuse:
        nodeTypeString = '|'
        totalresult = 0

        for nodeTestResult in nodeTestResults:
            totalresult += nodeTestResult['result']
            nodeTypeString += f"{nodeTestResult['type']}|"

        writer.writerow([f"{policy['type']}", f"{nodeTypeString}", f"{totalresult}", f"{upper_bound}", f"{lower_bound}", f"{repeats}"])
    else:
        for nodeTestResult in nodeTestResults:
            writer.writerow([f"{policy['type']}", f"{nodeTestResult['type']}", f"{nodeTestResult['result']}", f"{upper_bound}", f"{upper_bound > nodeTestResult['result']}"])
#------------------------------------------------------|

#------------------------------------------------------|
def evaluateResponseTimePercentile(policyTest : PolicyTest, policy, writer, project : Project):
    """
    Generates and writes results for the PolicyTest of type ResponseTimePercentile into the result file

    Args:
        - policyTest (PolicyTest) : The policyTest object to create results for
        - policy (dict) : The yaml represantation of the policy
        - writer (csv_writer) : A writer to write the results
    """
    nodeTestResults = []

    upper_bound = float(policy.get('properties')['upper_bound'])
    lower_bound = float(policy.get('properties')['lower_bound'])
    repeats = float(policy.get('properties')['repeats'])
    percentile = float(policy.get('properties')['percentile'])
    fuse = bool(policy.get('properties')['fuse'])

    # Fill NodeTestAverages into the list
    for nodeTest in policyTest.node_tests:
        nodeTemplate = json.loads(nodeTest.node)
        nodeTemplateType = nodeTemplate['type']

        resultPath = f"{nodeTest.artifact_path}results.csv"
        
        resultList = []
        # Get the results from the csv
        with open(resultPath, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                resultList.append(float(row[0]))

        #Get the value for the given percentile
        percentileValue = numpy.percentile(resultList, percentile)

        nodeTestEntry = {
            'type' : nodeTemplateType,
            'result' : mean(list(filter(lambda x: x <= percentileValue, resultList))),
        }

        nodeTestResults.append(nodeTestEntry)

    # Create the policyTest entry into the result
    if fuse:
        nodeTypeString = '|'
        totalresult = 0

        for nodeTestResult in nodeTestResults:
            totalresult += nodeTestResult['result']
            nodeTypeString += f"{nodeTestResult['type']}|"

        writer.writerow([f"{policy['type']}", f"{nodeTypeString}", f"{totalresult}", f"{upper_bound}", f"{lower_bound}", f"{repeats}", f"{percentile}"])
    else:
        for nodeTestResult in nodeTestResults:
            writer.writerow([f"{policy['type']}", f"{nodeTestResult['type']}", f"{nodeTestResult['result']}", f"{upper_bound}", f"{upper_bound}", f"{lower_bound}", f"{repeats}", f"{percentile}"])
#------------------------------------------------------|

#------------------------------------------------------|
def evaluateLoadTest(policyTest : PolicyTest, policy, writer, project : Project):
    """
    Generates and writes results for PolicyTest of type LoadTest into the result file

    Args:
        - policyTest (PolicyTest) : The policyTest object to create results for
        - policy (dict) : The yaml represantation of the policy
        - writer (csv_writer) : A writer to write the results
    """

    projectResultPath = f"{project.project_path}results{os.path.sep}"

    # For JMETER tests just copy the result file into the result directory
    for nodeTest in policyTest.node_tests:
        node = json.loads(nodeTest.node)
        nodeType = node['type']
    
        resultPath = f"{nodeTest.artifact_path}result.csv"
        targetFile = f"{projectResultPath}jmeter_test_{nodeTest.id}.csv"

        shutil.copyfile(resultPath,targetFile)

        writer.writerow([f"{nodeType}", targetFile])
#------------------------------------------------------|