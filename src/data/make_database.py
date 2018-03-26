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
    """
    CREATE TABLE IF NOT EXISTS "import_tweets" (
	    "id" bigint NOT NULL,
	    "created_at" TIMESTAMP NOT NULL,
	    "text" TEXT,
	    "user" TEXT NOT NULL,
	    "lang" varchar(2),
	    "coordinates" TEXT,
	    CONSTRAINT import_tweets_pk PRIMARY KEY ("id")
    ) WITH (
        OIDS=FALSE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS "filter_tweets" (
	    "id" bigint NOT NULL,
	    "created_at" TIMESTAMP NOT NULL,
	    "text" TEXT,
	    "user" TEXT NOT NULL,
	    "lang" varchar(2),
	    "coordinates" TEXT,
	    CONSTRAINT filter_tweets_pk PRIMARY KEY ("id")
    ) WITH (
        OIDS=FALSE
    );
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
