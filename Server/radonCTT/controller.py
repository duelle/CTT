#==================================================================|
"""
This modules methods are responsible for setting up radonCTT on the
System.
"""
#==================================================================|

import os
import logging

from radonCTT.config import radonCTTConfig
from radonCTT.database import databaseSession, initializeDatabase
from radonCTT.database.mapper import mapObjectsToDatabase

from swagger_server.__main__ import application

#This Starts us in debug mode
logging.basicConfig(level=logging.INFO)

#------------------------------------------------------|
def run():
    """
    The run method performs three steps to setup radonCTT:
        1. Creates required directories using paths from the config
        2. Initializes the database files and connections
        3. Maps Objects to tables in the database
    """
    createDirs()
    initializeDatabase()
    mapObjectsToDatabase()
#------------------------------------------------------|

#------------------------------------------------------|
def createDirs():
    """
    Creates required directories based on the paths from the radonCTTConfig 
    """

    # Base Dir
    directory = os.path.dirname(radonCTTConfig['PATHS']['Base_Dir'])
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Project Dir
    directory = os.path.dirname(radonCTTConfig['PATHS']['Project_Dir'])
    if not os.path.exists(directory):
        os.makedirs(directory)
#------------------------------------------------------|

#------------------------------------------------------|
@application.teardown_appcontext
def shutdown_session(exception=None):
    databaseSession.remove()
#------------------------------------------------------|
