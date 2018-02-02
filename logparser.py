import logging
import os
import json
import csv
import time
import sys

csv.field_size_limit(500 * 1024 * 1024)


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Change to your data model class after you edit the DataTemplate.py
from model import LogRecord

LOG_FORMAT = '%(asctime)-15s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

CONFIG_FILEPATH = 'config.json'
CSV_FILEPATH = os.path.join('data', 'testdata.log')
CSV_FILEPATH = os.path.join('data', 'full.log')
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

# Deal with CSV log file to avoid re-processing the same records tomorrow
local_datetime = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))

# new_csv_filename = CSV_FILEPATH[:-4] + '_{}.log'.format(local_datetime)

# Assuming this database operation will go ok, we can reset the log back to scratch and keep the old one around
# os.rename(CSV_FILEPATH, new_csv_filename)

# with open(new_csv_filename, 'r') as csvfile:
with open(CSV_FILEPATH, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    skipped_lines = 0
    while skipped_lines < NUM_HEADER_LINES_TO_SKIP:
        skipped_lines += 1
        next(csv_reader)

    # Load all the CSV lines into a list to get them in memory
    # Warning: don't use this if your log/csv is over 2GB or so
    csv_lines = [line for line in csv_reader]

skipped_records = 0
records_to_insert = []
for i, line in enumerate(csv_lines):
    curr = LogRecord.LogRecord(line)
    if i > 0:
        prev = LogRecord.LogRecord(csv_lines[i - 1])
        if curr.EpochFreq != prev.EpochFreq:
            records_to_insert.append(curr)
        else:
            logger.debug('Skipping line b/c it matches previous record: {}'.format(curr))
            skipped_records += 1
    else:
        # Add the first record
        records_to_insert.append(curr)

logger.info('Skipped {} records due to EpochFreq match.'.format(skipped_records))

# Create the table in postgres using the Class definition if it's not created already
SQLAlchBaseClass.metadata.create_all(db_engine)

for record in records_to_insert:
    logger.info(record.StartDateTime)
session.add_all(records_to_insert)
session.commit()
