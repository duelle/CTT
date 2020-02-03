#==================================================================|
"""
This module contains mappings of RadonCTT resources to DB-Tables.
"""
#==================================================================|
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from radonCTT.database import metadata
from swagger_server import models

#------------------------------------------------------|
# TABLE DEFINITIONS
#------------------------------------------------------|

projects = Table( 'projects', metadata,
    Column('_id', Integer, primary_key=True, autoincrement=True),
    Column('_status', String(20), unique=False),
    Column('_repository_url', String(250), unique=True),
    Column('_servicetemplate_location', String(250), unique=False),
    Column('_project_path', String(250), unique=True)
)

testartifacts = Table( 'testartifacts', metadata,
    Column('_id', Integer, primary_key=True, autoincrement=True),
    Column('_status', String(20), unique=False),
    Column('_project_id', Integer, unique=True),
)

policyTests = Table( 'policyTests', metadata,
    Column('_id', Integer, primary_key=True, autoincrement=True),
    Column('_status', String(20), unique=False),
    Column('_project_id', Integer, unique=False),
    Column('_testartifact_id', Integer, unique=False),
    Column('_policy', String(1000), unique=False),
)

nodeTests = Table( 'nodeTests', metadata,
    Column('_id', Integer, primary_key=True, autoincrement=True),
    Column('_status', String(20), unique=False),
    Column('_project_id', Integer, unique=False),
    Column('_policy_test_id', Integer, unique=False),
    Column('_node', String(1000), unique=False),
    Column('_artifact_path', String(250), unique=False),
)

deployments = Table( 'deployments', metadata,
    Column('_id', Integer, primary_key=True, autoincrement=True),
    Column('_status', String(20), unique=False),
    Column('_project_id', Integer, unique=True),
    Column('_testartifact_id', Integer, unique=True),
)

executors = Table( 'executors', metadata,
    Column('_id', Integer, primary_key=True, autoincrement=True),
    Column('_status', String(20), unique=False),
    Column('_project_id', Integer, unique=True),
    Column('_deployment_id', Integer, unique=True),
)

results = Table( 'results', metadata,
    Column('_id', Integer, primary_key=True, autoincrement=True),
    Column('_project_id', Integer, unique=True),
    Column('_testartifact_id', Integer, unique=True),
    Column('_result_path', String(250), unique=False),
) 

#------------------------------------------------------|
def mapObjectsToDatabase():
    """
    Maps our model-classes to their respective sql-table.
    At the same time, the tables are inserted into the DB.
    """

    mapper(models.Project, projects)
    mapper(models.Testartifact, testartifacts)
    mapper(models.PolicyTest, policyTests)
    mapper(models.NodeTest, nodeTests)
    mapper(models.Deployment, deployments)
    mapper(models.Executor, executors)
    mapper(models.Result, results)
#------------------------------------------------------|