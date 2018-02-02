import logging
import os
import json
import csv
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

gitrepo = False
try:
    from model import LogRecord
except:
    from model import DataTemplate

    gitrepo = True

LOG_FORMAT = '%(asctime)-15s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

CONFIG_FILEPATH = 'config.json'
CSV_FILEPATH = os.path.join('data', 'testdata.log')
NUM_HEADER_LINES_TO_SKIP = 3

# TEMPLATE: db_conn_string = 'postgres://username:pwd@localhost:5432/dbname'
db_conn_string = 'postgres://postgres:postgres@localhost:5432/logs'

db_engine = create_engine(db_conn_string)
SQLAlchBaseClass = declarative_base()
Session = sessionmaker(bind=db_engine)
session = Session()

def get_config_options(config_filepath):
    logger.debug('Loading Config file from: {}'.format(config_filepath))
    with open(config_filepath) as json_data_file:
        data = json.load(json_data_file)
    logger.info('Config data: {}'.format(data))
    return data


sql_session = sessionmaker(bind=db_engine)
SQLAlchBaseClass.metadata.create_all(db_engine)

local_datetime = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))

new_csv_filename = CSV_FILEPATH[:-4] + '_{}.log'.format(local_datetime)

# Assuming this database operation will go ok, we can reset the log back to scratch and keep the old one around
os.rename(CSV_FILEPATH, new_csv_filename)

with open(new_csv_filename, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",")
    skipped_lines = 0
    while skipped_lines < NUM_HEADER_LINES_TO_SKIP:
        skipped_lines += 1
        next(csv_reader)
    # Create a new object from every line in the CSV, using the rules defined within the class's init method
    records_to_insert = [LogRecord.LogRecord(line) for _, line in enumerate(csv_reader)]

# Create the table in postgres using the Class definition if it's not created already
SQLAlchBaseClass.metadata.create_all(db_engine)

for record in records_to_insert:
    logger.info(record.StartDateTime)
session.add_all(records_to_insert)
session.commit()
