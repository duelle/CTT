#==================================================================|
"""
A Temporary parser which simply reads in a yml file and places it
into a global variable.
"""
#==================================================================|

import yaml

# A Dictionary containing the serviceTemplate. See the "tosca_file_structure.txt" file for 
# reference on how a tosca file and thus this dictionary is structured.
serviceTemplate = {}

#------------------------------------------------------|
def parse(serviceTemplatePath: str):
    """ 
    Parses a given yaml file and puts it in the global serviceTemplate variable.
    Does not check if the yaml file has a valid TOSCA format.

    Args:
        serviceTemplatePath (str): The file location of the service template
    """

    with open(serviceTemplatePath, 'r') as stream:
        try:
            global serviceTemplate
            serviceTemplate = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
#------------------------------------------------------|

#------------------------------------------------------|
def getNodeTemplates():
    """ 
    Returns the node templates contained in a service template

    Returns:
        A Dictionary containing the node templates or None if no template has been parsed.
    """

    global serviceTemplate
    if not serviceTemplate:
        return None
    else:
        return serviceTemplate.get('topology_template', {}).get('node_templates')
#------------------------------------------------------|

#------------------------------------------------------|
def getPolicies():

    """ 
    Returns the policies contained in a topology section of a service template

    Returns:
        A Dictionary containing the policies or None if no template has been parsed.
    """

    global serviceTemplate
    if not serviceTemplate:
        return None
    else:
        return serviceTemplate.get('topology_template', {}).get('policies')
#------------------------------------------------------|