# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from io import StringIO
from time import time


def get_twitter_files(input_filepath):
    """ Returns a list of all .csv files in the input directory.
        :param: input_filepath - File path to directory containing raw twitter scrapes.
        :returns: List of .csv filepaths for importing.
    """
    log_main = logging.getLogger(__name__)
    log_files = log_main.getChild('find_files')
    log_files.info('Gathering files to import.')

    filtered_files = []

    try:
        files = os.listdir(input_filepath)

        # Filter log files keeping only csv/non-hidden files
        filtered_files = [f for f in files if \
            (f.endswith('.csv') and not f.startswith('.'))]

        # Create file paths by combining it with our passed directory
        filtered_files = [os.path.join(input_filepath, f) for f in filtered_files]

    except Exception as error:
        print ('\tCould not find directory!')
        print ('\tError: ', error)
    
    finally:
        return filtered_files


def import_file(filepath, db):
    """ Function that imports a file into our database using the native COPY
        command. 
        :param: filepath - Valid filepath
        :param: db - Database connection from SQLAlchemy.
        :returns: Boolean indicating if the file was sucessfully uploaded.
    """
    # Logging
    log_main = logging.getLogger(__name__)
    log_import = log_main.getChild(filepath.split('/')[-1])
    log_import.info('started')
    start = time()

    # Variables used in data processing
    memory_buff = StringIO()
    curr        = None
    cols        = ['tweetID', 'date', 'message', 'username', 'userID', 'language',
                    'longitude', 'latitude', 'retweet']
    sql = """COPY "raw_tweets" ("tweetID", "date", "message", "username", "userID", "language", "longitude", "latitude", "retweet") 
    FROM STDIN 
    WITH (FORMAT CSV, HEADER TRUE, DELIMITER '\t');
    """
    
    # Try reading the file
    try:
        df = pd.read_csv(filepath, usecols=cols, engine='c', 
                        dtype={'userID': np.int64, 'tweetID': np.int64})
    except Exception as e:
        log_import.warn('error on read_csv')
        memory_buff.close()
        print (e)
        return

    # Attempt to open up a connection to database.
    try:
        conn = db.raw_connection()
        curr = conn.cursor()
    except (Exception) as e:
        log_import.warn('error on server connection')
        memory_buff.close()
        if curr is not None:
            curr.close()
        print (e)
        return

    # Try copying the files to table.
    try:
        # Save to our buffer
        df[cols].to_csv(memory_buff, sep='\t',
                        header=True, index=False, encoding='utf-8')

        # Point buffer to start of memory block
        memory_buff.seek(0)

        # Copy records using native Postgres COPY command (FAST)
        curr.copy_expert(sql, memory_buff)

        # Save transaction and commit to DB
        conn.commit()
    except (Exception) as e:
        log_import.warn('error while copying to database')
        memory_buff.close()
        if curr is not None:
            curr.close()
        print (e)
        return
    finally:
        memory_buff.close()
        if curr is not None:
            curr.close()
    log_import.info('finished ({})'.format((time() - start) / 1000))
    return


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True), envvar='DATA_DIR')
@click.argument('output_filepath', type=click.Path(), default='.')
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    # Logging set up
    start = time()
    logger = logging.getLogger(__name__)
    logger.info('Making final data set from raw data\ngathering file names...')
    
    # Dataset variables
    import_url = os.environ.get('IMPORT_URL')
    db_engine = create_engine(import_url, client_encoding='utf8')
    csvs = get_twitter_files(input_filepath)
    
    # Upload data
    logger.info('Starting to upload {} csvs...'.format(len(csvs)))
    with click.progressbar(csvs, label='CSV Imports: ') as csv_progress:
        for csv in csv_progress:
            import_file(csv, db_engine)

    logger.info('{} files done in {} secs.'.format(len(csvs), time() - start))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, 
                    format=log_fmt, datefmt='%H:%M:%S',
                    filename='pipeline.log', filemode='w')

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    
    # Clear terminal before outputting a bynch of logs
    #click.clear()

    main()
