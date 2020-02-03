#==================================================================|
"""
This module contains logic to create radonCTTs DB.
"""
#==================================================================|
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

from swagger_server import models

from radonCTT.config import radonCTTConfig

engine = create_engine(f"sqlite:///{radonCTTConfig['PATHS']['Database_Path']}", convert_unicode=True)
metadata = MetaData()
databaseSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

#------------------------------------------------------|
def initializeDatabase():
    """
    Initializes the Database
    """
    metadata.create_all(bind=engine)
#------------------------------------------------------|



