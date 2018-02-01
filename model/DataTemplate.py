import logging

from sqlalchemy import Column, String, Integer, Time, Float
from sqlalchemy.ext.declarative import declarative_base

LOG_FORMAT = '%(asctime)-15s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

SQLAlchBaseClass = declarative_base()

class LogRecord(SQLAlchBaseClass):
    logger.debug('Creating Log Record Class for SQL Alch')
    __tablename__ = 'logstemplate'
    id = Column(Integer, primary_key=True)
    Group = Column(String)
    Num = Column(Float)
    Tone = Column(String)
    Type2 = Column(Integer)
    IDTest = Column(String)
    Type4 = Column(String)
    NumLogs = Column(Integer)
    TimeUp = Column(Time)
    StartDateTime = Column(String)
    Group1Name = Column(String)
    Group2Name = Column(String)
    Group3Name = Column(String)
    Group4Name = Column(String)
    GroupType = Column(String)
