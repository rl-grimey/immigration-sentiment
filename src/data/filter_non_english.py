""" filter_non_english.py
    
    Python script to ultimately filter non-English tweets from our 
    filtered_tweets table. This script uses the Python library langid
    to classify the tweet's language.
"""

###############################################################################
# Libraries                                                                   #
###############################################################################
# Environment + Database variables
import os
from dotenv import find_dotenv, load_dotenv
import psycopg2 as pg

# Used to import from parent packages: HACKY
import sys
sys.path.append('src/utils')
import twokenize

# Data + language processing
import pandas.io.sql as psql
import langid
import re


###############################################################################
# Global variables                                                            #
###############################################################################
# For cleaning tweets
to_clean = re.compile(twokenize.regex_or(
  twokenize.Hearts,
  twokenize.url,
  twokenize.Email,
  twokenize.emoticon,
  twokenize.Arrows,
  twokenize.entity,
  twokenize.decorations,
  twokenize.Hashtag,
  twokenize.AtMention,
), re.UNICODE)

# For SQL ingestion
message_sql = 'SELECT "tweetID", "message" FROM filter_tweets LIMIT 10000;'


###############################################################################
# Functions                                                                   #
###############################################################################
# For cleaning tweets
to_clean = re.compile(twokenize.regex_or(
  twokenize.Hearts,
  twokenize.url,
  twokenize.Email,
  twokenize.emoticon,
  twokenize.Arrows,
  twokenize.entity,
  twokenize.decorations,
  twokenize.Hashtag,
  twokenize.AtMention,
), re.UNICODE)

def clean_tweet(text):
    """For preprocessing classification"""
    return to_clean.sub('', text)

def squeeze_whitespace(text):
    """For printing tweets."""
    return re.sub('\s+', ' ', text)

def langid_clf(text):
    """ Function to clean a tweet and return the most probable language."""
    cleaned = clean_tweet(text)
    return langid.classify(cleaned)[0]

def format_filter(df):
    """ Function to format a SQL command with a list of IDs taken from a dataframe.
    """
    # Gather non english tweets into a list
    non_english_mask = df[df.langid != 'en']
    tweet_ids_list = non_english_mask['tweetID'].astype(str).values.tolist()
    tweet_ids_str = ', '.join(['('+c+')' for c in tweet_ids_list])
    
    print('{} non-english tweets.'.format(len(tweet_ids_list)))
    
    # For getting rid of the tweets: use tweetIDs to drop from database.
    # https://www.datadoghq.com/blog/100x-faster-postgres-performance-by-changing-1-line/
    filter_sql = 'DELETE FROM filter_tweets WHERE "tweetID" = ANY (VALUES {});'.format(tweet_ids_str)
    
    return filter_sql


###############################################################################
# Filtering                                                                   #
###############################################################################

if __name__ == '__main__':
    # load environment
    load_dotenv(find_dotenv())
    
    # Set up database
    database_url = os.environ.get('DATABASE_URL')
    conn = pg.connect(database_url)
    curr = conn.cursor()
    
    # Grab messages
    message_df = psql.read_sql(message_sql, conn)
    
    # Classify the language
    message_df['langid'] = message_df.message.apply(lambda x: langid_clf(x))
    
    # Use new column to create SQL command
    filter_sql = format_filter(message_df)
    
    # PSYCOPG2 error
    # > target lists can have at most 1664 entries
    # > changing the limit to 1664 brings new error: syntax error near ANY
    curr.execute(filter_sql)
    conn.commit()
    
    # Close up shop
    curr.close()
    conn.close()