import logging

from sqlalchemy import Column, String, Integer, Time, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

LOG_FORMAT = '%(asctime)-15s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

db_conn_string = 'postgres://postgres:postgres@localhost:5432/logs'
db_engine = create_engine(db_conn_string)
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

    def __init__(self, line):
        self.Group = line[0]
        self.Num = line[1].lstrip()
        self.Tone = line[2].lstrip()
        self.Type2 = int(line[3].lstrip())
        self.IDTest = line[4].lstrip()
        self.Type4 = line[5].lstrip()
        self.NumLogs = int(line[6].lstrip())
        self.TimeUp = line[7].lstrip()
        self.StartDateTime = line[8].lstrip()
        self.Group1Name = line[9].split(' - ')[0].lstrip()
        self.Group2Name = line[9].split(' - ')[1].lstrip()
        self.Group3Name = str(line[9].split(' - ')[2:]).lstrip()
        self.Group4Name = line[10].lstrip()
        self.GroupType = line[11].lstrip()

SQLAlchBaseClass.metadata.create_all(db_engine)
