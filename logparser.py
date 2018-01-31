import logging
import os
import json

from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

LOG_FORMAT = '%(asctime)-15s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# db_conn_string = 'postgres://username:pwd@localhost:5432/dbname'
db_conn_string = 'postgres://postgres:postgres@localhost:5432/logs'

db_engine = create_engine(db_conn_string)
sql_alch_base = declarative_base()


def get_config_options(config_filepath):
    print('Load config')
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    print('Create: {}'.format(data))
    return data


class LogRecord(sql_alch_base):
    print('Create SQL Alchemy class for records')
    field_config = get_config_options('')

    __tablename__ = 'logs1'
    for field_mapping in field_config.items():
        print(field_mapping)
    field1 = Column(String, primary_key=True)
    field2 = Column(String)
    field3 = Column(String)
    field4 = Column(String)
