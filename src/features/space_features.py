""" space_features.py

    Creates a table within the database to map tweetIDs -> U.S. County GeoID.
    Outer Left Join is accomplished by intersecting tweet's lat/lng + 
    U.S. County polygon.
"""

###############################################################################
# Libraries                                                                   #
###############################################################################

# Environment + Database variables
import os, sys
from dotenv import find_dotenv, load_dotenv
import psycopg2 as pg

# Data processing
import pandas.io.sql as psql


###############################################################################
# Global variables                                                            #
###############################################################################

# For clearing the database each iteration
create_sql = """
    DROP TABLE IF EXISTS "features_space" CASCADE;
    CREATE TABLE "features_space" (
        "tweetID" BIGINT NOT NULL,
        "geoid" VARCHAR(5) REFERENCES counties (geoid),
        CONSTRAINT features_space_pk PRIMARY KEY ("tweetID")
    ) WITH ( OIDS=FALSE );
"""

# For creating new table based on tweets <=> locations
cnty_intersect_sql =  """
INSERT INTO 
    features_space 
SELECT 
    filter_tweets."tweetID",
    counties.geoid 
FROM
    filter_tweets 
LEFT OUTER JOIN
    counties 
ON
    ST_Intersects(
        ST_SetSRID(
            ST_MakePoint(filter_tweets.longitude, filter_tweets.latitude), 
            4326),
        counties.geom
    );
"""



if __name__ == '__main__':
    # Load user env
    load_dotenv(find_dotenv())
    
    # Set up database
    database_url = os.environ.get('DATABASE_URL')
    conn = pg.connect(database_url)
    curr = conn.cursor()
    
    try:
        # Clear table
        curr.execute(create_sql)
        conn.commit()
        
        # Create table from geographic intersection of tweets and counties
        curr.execute(cnty_intersect_sql)
        conn.commit()
    
    except (Exception) as e:
        print (e)
    
    finally:
        if not curr.closed: curr.close()
        if conn: conn.close()
    
    print ('\tSpacial features complete!')