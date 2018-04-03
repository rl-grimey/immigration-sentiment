# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import psycopg2 as pg


###############################################################################
# Postgres Queries                                                            #
###############################################################################

filters = {
    'total': '("tweetID" IS NOT NULL)',
    'message': '(message IS NOT NULL)',
    'retweet': '(retweet IS NULL)',
    'language': "(LEFT(language, 2) LIKE 'en')",
    'date': "(date >= '2016-12-30 04:00:00' AND date < '2017-02-24 04:00:00')",
    'location': '((latitude IS NOT NULL) AND (longitude IS NOT NULL))'
}

filter_query = """
INSERT INTO
    filter_tweets
SELECT 
    DISTINCT ON ("tweetID") 
    * 
FROM 
    raw_tweets
WHERE
    (message IS NOT NULL) AND
    (retweet IS NULL) AND
    (LEFT(language, 2) LIKE 'en') AND
    (latitude IS NOT NULL) AND
    (longitude IS NOT NULL);
"""


###############################################################################
# Postgres Table Creation                                                     #
###############################################################################

def main():
    """
    """
    # Logging set up
    logger = logging.getLogger(__name__)
    log_filter = logger.getChild('filter_tweets')
    logger.info('Updating filtered table from raw_tweets.')

    # Database variables
    database_url = os.environ.get('DATABASE_URL')
    conn = pg.connect(database_url)
    curr = conn.cursor()

    # Drop tweets from existing table for now
    #curr.execute('DELETE FROM filter_tweets WHERE "tweetID" IS NOT NULL;')

    # Get filter counts
    log_filter.info('getting filtered counts')
    for col in filters.keys():
        query = 'SELECT COUNT(*) FROM raw_tweets WHERE ' + filters[col] + ';'
        curr.execute(query)

        filter_cnt = curr.fetchone()[0]
        log_filter.info('Filter: {}  [{}]: {}'.format(col, query, filter_cnt))
        print ('\t{}:\t{}'.format(col, filter_cnt))

    # Create filtered tweets table
    logger.info('Inserting valid tweets into filter_tweets table.')
    curr.execute(filter_query)

    # Grab count from table
    curr.execute('SELECT COUNT(*) FROM filter_tweets;')
    total_filtered_cnt = curr.fetchone()[0]
    log_filter.info('{} tweets inserted into filter_tweets'.format(total_filtered_cnt))
    
    # Close up
    conn.close()
    

if __name__ == '__main__':
    # Configure logging
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, 
                    format=log_fmt, datefmt='%H:%M:%S',
                    filename='reports/pipeline.filter.log', filemode='a')

    # Load our dot environment
    load_dotenv(find_dotenv())

    main()