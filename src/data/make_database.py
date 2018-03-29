import os
import logging
from dotenv import load_dotenv, find_dotenv
import psycopg2 as pg


###############################################################################
# Environment variables                                                       #
###############################################################################

def get_env_url():
    """Function returning our environment variables if found."""
    
    print ('\tFinding environment variables from .env...')

    try:
        # find .env automagically by walking up directories until it's found
        dotenv_path = find_dotenv()

        # load up the entries as environment variables
        load_dotenv(dotenv_path)

        # Gather variables for database.
        database_url = os.environ.get("DATABASE_URL")

        return database_url
    except Exception as error:
        print ('\tCould not find environment files!')
        print ('\tError: ', error)


###############################################################################
# Postgres Schemas                                                            #
###############################################################################

schemas = (
    #"""DROP TABLE "filter_tweets";""",
    #"""DROP TABLE "raw_tweets";""",
    """
    CREATE TABLE IF NOT EXISTS "raw_tweets" (
        "id" SERIAL NOT NULL,
	    "tweetID" BIGINT NOT NULL,
	    "date" TIMESTAMP,
	    "message" TEXT,
	    "username" TEXT,
        "userID" BIGINT NOT NULL,
	    "language" VARCHAR(10),
	    "longitude" FLOAT,
        "latitude" FLOAT,
        "retweet" TEXT,
	    CONSTRAINT raw_tweets_pk PRIMARY KEY ("id")
    ) WITH (
        OIDS=FALSE
    );
    """,
    # In the filtered table we should set the column values.
    """
    CREATE TABLE IF NOT EXISTS "filter_tweets" (
        "id" SERIAL NOT NULL,
	    "tweetID" BIGINT NOT NULL,
	    "date" TIMESTAMP,
	    "message" TEXT,
	    "username" TEXT,
        "userID" BIGINT NOT NULL,
	    "language" VARCHAR(10),
	    "longitude" FLOAT,
        "latitude" FLOAT,
        "retweet" TEXT
    ) WITH (
        OIDS=FALSE
    );
    """,
    """
    ALTER TABLE "filter_tweets" ADD CONSTRAINT "filter_fk0" FOREIGN KEY ("id") REFERENCES "raw_tweets"("id");
    """
)


###############################################################################
# Postgres Table Creation                                                     #
###############################################################################
def create_tables(url):
    """Make a table in our Postgres database."""
    global schemas

    # Create a database connection pointer
    conn = None
    print ('\tAttemping to connect to database...')

    try:
        # Connect to the PostgreSQL server
        conn = pg.connect(url)
        cur = conn.cursor()
        print ('\tConnected! Creating tables...')

        # Create tables from schemas
        for schema in schemas:
            cur.execute(schema)

        # Close communication, close connection to SQL server.
        cur.close()
        conn.commit()
    
    except (Exception, pg.DatabaseError) as error:
        print ('\tConnection failed!')
        print ('\tError: ', error)
    
    finally:
        if conn is not None:
            print ('\tClosing PostgreSQL database connection.')
            conn.close()

if __name__ == '__main__':
    print ('01. Creating Postgres Tables.')
    database_url = get_env_url()
    create_tables(database_url)
