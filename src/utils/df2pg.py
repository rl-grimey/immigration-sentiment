""" df2pg.py

    DataFrame to PostgreSQL Python script. Inserts a pandas dataframe into a 
    Postgres database table via memoryIO instead of writing to file.
"""

import os
import pandas as pd
from io import StringIO
from time import time

def process_cols(cols):
    """ Function to format a list of strings into SQL columns.
        > ['tweetID', 'date', 'message'] => '("tweetID", "date", "message")' 

        Args:
            cols (list[str]): List of strings.

        Returns:
            sql (str): Columns in SQL string format.
    """
    cols_w_quotes = ['"' + c + '"' for c in cols]
    sql = '(' + ', '.join(cols_w_quotes) + ')'
    return sql


def df2pg(df, cols, db, table):
    """ Inserts a dataframe to PostgreSQL table. Leverages PSQL's COPY 
        function to increase speed. We use memory IO to save write time.

        Args:
            df (pandas.DataFrame): Dataframe to insert.
            cols (list): Ordered list of strings, matching database table.
            db (SQLAlchemy): Database connection cursor.
            table (str): Name of table to insert to.

        Returns:
            success (bool): Boolean indicating success.
    """
    # Gather variables
    sql_cmd = """COPY {} {} FROM STDIN 
    WITH (FORMAT CSV, HEADER TRUE, DELIMITER '\t');""".format(table, process_cols(cols))
    memory_buffer = StringIO()
    

    return start