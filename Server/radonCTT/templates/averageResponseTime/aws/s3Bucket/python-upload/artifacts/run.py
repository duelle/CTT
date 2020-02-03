#==================================================================|
"""
This python module measures how long it takes to upload to a s3 
bucket and puts the results in a csv.
"""
#==================================================================|

import sys
import time
import boto3
import shutil
import subprocess
import csv
import logging
import timeit
from timeit import default_timer as timer

s3 = boto3.client('s3')
activeFileName = ''
durations = []

# Variables filled through CLI arguments ---|
REPEATS = 0 # ARG 1
SOURCE_FILE_PREFIX = '' # ARG 2
SOURCE_FILE_POSTFIX = '' # ARG 3
BUCKET_NAME = '' # ARG 4
SOURCE_FILE_PATH = '' # ARG 5
RESULT_PATH =  '' #ARG 6
UNIQUE_TEST_ID = '' #ARG 7
# ------------------------------------------|

def runTest():
    global REPEATS, SOURCE_FILE_PREFIX, SOURCE_FILE_POSTFIX, BUCKET_NAME, SOURCE_FILE_PATH, RESULT_PATH, UNIQUE_TEST_ID

    REPEATS = int(sys.argv[1])

    SOURCE_FILE_PREFIX = f"{sys.argv[2]}"

    SOURCE_FILE_POSTFIX = f"{sys.argv[3]}"

    BUCKET_NAME = f"{sys.argv[4]}"

    SOURCE_FILE_PATH = f"{sys.argv[5]}"

    RESULT_PATH = f"{sys.argv[6]}"

    UNIQUE_TEST_ID = f"{sys.argv[7]}"


    for index in range(REPEATS):
        prepareNextFile(index)
        durations.append(timeit.timeit(uploadFile, number = 1))

    generateResult()

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


def uploadFile():
    global BUCKET_NAME, activeFileName

    s3.upload_file(activeFileName, BUCKET_NAME, activeFileName)

def generateResult():
    with open(f"{RESULT_PATH}results.csv", 'w+') as csv_file:
        csvWriter = csv.writer(csv_file, delimiter=';',quotechar='"', quoting = csv.QUOTE_MINIMAL)
        for duration in durations:
            csvWriter.writerow([duration])

# +~+~+~+~+~ XOPERA ENTRYPOINT +~+~+~+~+~ #
runTest()
# +~+~+~+~+~ XOPERA ENTRYPOINT +~+~+~+~+~ #

    