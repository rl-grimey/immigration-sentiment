""" build_features.py

    Creates a features table in the database by joining our smaller feature
    tables on their primary keys (tweetIDs).
"""

###############################################################################
# Libraries                                                                   #
###############################################################################

# Environment + Database variables
import os, sys
from dotenv import find_dotenv, load_dotenv
import psycopg2 as pg


###############################################################################
# Global variables                                                            #
###############################################################################

create_sql = """
    DROP TABLE IF EXISTS "features" CASCADE;
    CREATE TABLE "features" (
        "tweetID" BIGINT NOT NULL,
        "message" TEXT NOT NULL,
        "geoid" VARCHAR(5) NOT NULL REFERENCES counties (geoid),
        "date" TIMESTAMP NOT NULL,
        "period" INT NOT NULL,
        CONSTRAINT features_pk PRIMARY KEY ("tweetID")
    ) WITH ( OIDS=False );
"""

join_sql = """
INSERT INTO 
    features 
SELECT 
    features_lang."tweetID",
    features_lang.message,
    features_space.geoid,
    features_time.date,
    features_time.period
FROM
    features_lang,
    features_space,
    features_time 
WHERE
    (features_lang."tweetID" = features_space."tweetID" AND
        features_space."tweetID" = features_time."tweetID") AND
    (features_lang.langid = 'en') AND
    (features_space.geoid IS NOT NULL) AND
    (features_time.period IS NOT NULL);
"""


if __name__ == '__main__':    
    # Load user env
    load_dotenv(find_dotenv())
    
    # Set up database
    database_url = os.environ.get('DATABASE_URL')
    conn = pg.connect(database_url)
    curr = conn.cursor()
    
    # Read in all of the feature tables and combine them
    try:
        # Clear the way for complete feature table
        curr.execute(create_sql, conn)
        conn.commit()
        
        curr.execute(join_sql)
        conn.commit()
        
        # if instead you wanted to analyze in pandas
        #joined = psql.read_sql_query(join_sql, conn)
        #print (joined.head())
        
    except (Exception) as e:
        print (e)
    
    finally:
        if not curr.closed: curr.close()
        if conn: conn.close()
