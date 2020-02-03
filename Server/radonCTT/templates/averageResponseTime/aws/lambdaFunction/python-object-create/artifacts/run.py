#==================================================================|
"""
This python module triggers a s3Bucket ObjectCreate event for a 
lambda function and then gets the execution time from aws cloudwatch
logs. Fills the durations into a csv.
"""
#==================================================================|

import sys
import time
import boto3
import shutil
import subprocess
import csv
from timeit import default_timer as timer

s3 = boto3.client('s3')
logs = boto3.client('logs')
query_string = 'filter @type = \"REPORT\" | fields @requestId, @duration, @timestamp | sort by @timestamp desc'
activeFileName = ''
durations = []

# Variables filled through CLI arguments ---|
REPEATS = 0 # ARG 1
FUNCTION_NAME = '' # ARG 2
SOURCE_FILE_PREFIX = '' # ARG 3
SOURCE_FILE_POSTFIX = '' # ARG 4
BUCKET_NAME = '' # ARG 5
SOURCE_FILE_PATH = '' # ARG 6
RESULT_PATH =  '' #ARG 7
UNIQUE_TEST_ID = '' #ARG 8
# ------------------------------------------|

def runTest():
    fillVariables()

    for index in range(REPEATS):
        prepareNextFile(index)
        uploadActiveFile()
        #Sleep between uploads
        time.sleep(1)


    #Wait 90 seconds before generating results
    time.sleep(90)
    generateResult()

def fillVariables():
    global REPEATS, FUNCTION_NAME, SOURCE_FILE_PREFIX, SOURCE_FILE_POSTFIX, BUCKET_NAME, SOURCE_FILE_PATH, RESULT_PATH, UNIQUE_TEST_ID, query_string

    REPEATS = int(sys.argv[1])

    FUNCTION_NAME = f"/aws/lambda/{sys.argv[2]}"

    SOURCE_FILE_PREFIX = f"{sys.argv[3]}"

    SOURCE_FILE_POSTFIX = f"{sys.argv[4]}"

    BUCKET_NAME = f"{sys.argv[5]}"

    SOURCE_FILE_PATH = f"{sys.argv[6]}"

    RESULT_PATH = f"{sys.argv[7]}"

    UNIQUE_TEST_ID = f"{sys.argv[8]}"

def prepareNextFile(index):
    global SOURCE_FILE_PREFIX, SOURCE_FILE_POSTFIX, UNIQUE_TEST_ID, activeFileName

    if index == 0:
        shutil.copyfile(f"{SOURCE_FILE_PATH}", f"{UNIQUE_TEST_ID}{SOURCE_FILE_PREFIX}{SOURCE_FILE_POSTFIX}")
        activeFileName = f"{UNIQUE_TEST_ID}{SOURCE_FILE_PREFIX}{SOURCE_FILE_POSTFIX}"
        return None
    
    if index == 1:
        oldFileName = f"{UNIQUE_TEST_ID}{SOURCE_FILE_PREFIX}{SOURCE_FILE_POSTFIX}"
    else:
        oldFileName = f"{UNIQUE_TEST_ID}{SOURCE_FILE_PREFIX}{index - 1}{SOURCE_FILE_POSTFIX}"

    activeFileName = f"{UNIQUE_TEST_ID}{SOURCE_FILE_PREFIX}{index}{SOURCE_FILE_POSTFIX}"

    shutil.copyfile(oldFileName, activeFileName)


def uploadActiveFile():
    global BUCKET_NAME, activeFileName

    s3.upload_file(activeFileName, BUCKET_NAME, activeFileName)

def generateResult():
    global FUNCTION_NAME, REPEATS, query_string

    # Getting results from Cloudwatch is fickle, thus have extensive retry logic ------------------------|
    retrievedResults = False

    while not retrievedResults:
        retryCounter = 0
        retryActiveQuery = True

        end_time = int(time.time())
        start_time = end_time - (60 * 60)

        startQueryResponse = logs.start_query(
            logGroupName=FUNCTION_NAME,
            startTime= start_time,
            endTime=end_time,
            queryString=query_string,
            limit=REPEATS,
        )

        # Wait before trying to get query results
        time.sleep(2)

        while retryActiveQuery:
            getQueryResponse = logs.get_query_results(queryId=f"{startQueryResponse['queryId']}")

            if getQueryResponse['results']:
                retrievedResults = True
                retryActiveQuery = False
            else :
                time.sleep(2)
                retryCounter += 1

                if retryCounter == 3:
                    retryActiveQuery = False
    #-------------------------------------------------------------------------------------------------------|


    for result in getQueryResponse['results']:
        for field in result:
            if field['field'] == '@duration':
                duration = field['value']
                durations.append(field['value'])

    with open(f"{RESULT_PATH}results.csv", 'w+') as csv_file:
        csvWriter = csv.writer(csv_file, delimiter=';',quotechar='"', quoting = csv.QUOTE_MINIMAL)
        for duration in durations:
            seconds = float(duration) / 1000
            csvWriter.writerow([seconds])

# +~+~+~+~+~ XOPERA ENTRYPOINT +~+~+~+~+~ #
runTest()
# +~+~+~+~+~ XOPERA ENTRYPOINT +~+~+~+~+~ #