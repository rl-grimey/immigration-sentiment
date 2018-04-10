""" lang_features.py
    
    Classifies messages' language. Useful for turning down the noise in our
    dataset.
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
from df2pg import df2pg

# Data processing
import pandas.io.sql as psql
import re
import langid

###############################################################################
# Global variables                                                            #
###############################################################################

# Clear out and create table in database 
create_sql = """
    DROP TABLE IF EXISTS "features_lang" CASCADE;
    CREATE TABLE "features_lang" (
        "tweetID" BIGINT NOT NULL,
        "message" TEXT NOT NULL,
        "langid" VARCHAR(2) NOT NULL,
        CONSTRAINT features_lang_pk PRIMARY KEY ("tweetID")
    ) WITH ( OIDS=FALSE );
"""

# Select filtered_tweets subset 
select_sql = 'SELECT "tweetID", "message" FROM filter_tweets;'

# New table columns
cols = ['tweetID', 'message', 'langid']

# Regex for cleaning tweets before language classification
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


###############################################################################
# Functions                                                                   #
###############################################################################

def clean_tweet(text):
    """ Splits a token in a list using Regex for preprocessing 
        language classification. """
    return to_clean.sub('', text)

def squeeze_whitespace(text):
    """For printing tweets."""
    return re.sub('\s+', ' ', text)

def langid_clf(text):
    """ Function to clean a tweet and return the most probable language."""
    cleaned = clean_tweet(text)
    return langid.classify(cleaned)[0]



if __name__ == '__main__':
    # Load user env
    load_dotenv(find_dotenv())
    
    # Set up database connection
    database_url = os.environ.get('DATABASE_URL')
    conn = pg.connect(database_url)
    curr = conn.cursor()
    
    try:
        # clear/create table
        curr.execute(create_sql)
        conn.commit()
        
        # Classify languages
        message_df = psql.read_sql(select_sql, conn)
    
        # Classify the language
        message_df['langid'] = message_df.message.apply(lambda x: langid_clf(x))
        
        # upload to DB as new table
        copy_success = df2pg(message_df, cols, curr, 'features_lang')
        if copy_success: 
            conn.commit()
        
    except (Exception) as e:
        print (e)
    
    finally:
        if not curr.closed: curr.close()
        if conn: conn.close()
    
    print ('\tLanguage features complete!')