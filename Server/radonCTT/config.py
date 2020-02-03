#==================================================================|
"""
This module allows access to this apps configuration by importing
the global radonCTTConfig variable.

Before using it, the config must be loaded with the loadConfig() method.

If it is being loaded for the first time, a default config will be created:
    -Windows:
        Config paths will be initialized to C:\\RadonCTT\\
    -Linux:
        Config paths will be initialized to /tmp/RadonCTT/

Config sections:
    -PATHS:
        -Base_Dir
        -Project_Dir
        -Database_Path
"""
#==================================================================|

import os 
import configparser
import logging

configPath = 'radonCTT.ini'

#------------------------------------------------------|
def loadConfig():
    """
    Loads the configfile and returns it. If no configfile
    exists yet, it creates one and initializes the paths
    based on the current os.
    """

    config = configparser.ConfigParser()

    if not os.path.exists(configPath):
        if os.name == 'nt':
            createDefaultConfigWindows()
            return
        else: 
            createDefaultConfigLinux()
            return

    config.read(configPath)

    return config
#------------------------------------------------------|

#------------------------------------------------------|
def createDefaultConfigWindows():
    """
    Creates a radonCTT.ini config file and saves it in the 
    default windows path. The resulting config is accessible 
    in the radonCTTConfig variable.
    """

    config = configparser.ConfigParser()
    config['PATHS'] = { 'Base_Dir' : 'C:\\RadonCTT\\',
                        'Project_Dir' : 'C:\\RadonCTT\\projects\\',
                        'Database_Path' : 'C:\\RadonCTT\\radonctt.db'}
    with open ('radonCTT.ini', 'w') as configfile:
        config.write(configfile)
#------------------------------------------------------|

#------------------------------------------------------|
def createDefaultConfigLinux():
    """
    Creates a radonCTT.ini config file and saves it in the 
    default Linux path. The resulting config is accessible 
    in the radonCTTConfig variable.
    """
    
    config = configparser.ConfigParser()
    config['PATHS'] = { 'Base_Dir' : '/tmp/RadonCTT/',
                        'Project_Dir' : '/tmp/RadonCTT/projects/',
                        'Database_Path' : '/tmp/RadonCTT/radonctt.db'}
    with open ('radonCTT.ini', 'w') as configfile:
        config.write(configfile)
#------------------------------------------------------|

radonCTTConfig = loadConfig()