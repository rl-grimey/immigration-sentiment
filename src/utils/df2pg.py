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


def df2pg(df, cols, curr, table):
    """ Inserts a dataframe to PostgreSQL table. Leverages PSQL's COPY 
        function to increase speed. We use memory IO to save write time.

        Args:
            df (pandas.DataFrame): Dataframe to insert.
            cols (list): Ordered list of strings, matching database table.
            curr (SQLAlchemy): Database connection cursor.
            table (str): Name of table to insert to.

        Returns:
            success (bool): Boolean indicating success.
    """
    # Database variables
    sql_cmd = """COPY {} {} FROM STDIN 
    WITH (FORMAT CSV, HEADER TRUE, DELIMITER '\t');""".format(table, process_cols(cols))
    memory_buffer = StringIO()
    success = True
    
    # Save routine
    try:      
        # Save to our buffer
        df[cols].to_csv(memory_buffer, sep='\t',
                        header=True, index=False, encoding='utf-8')

        # Point buffer to start of memory block
        memory_buffer.seek(0)

        # Copy records using native Postgres COPY command (FAST)
        curr.copy_expert(sql_cmd, memory_buffer)

        # Save transaction and commit to DB
        #conn.commit()
    
    except (Exception) as e:
        success = False
        print (e)
        
    finally:
        memory_buffer.close()
        if curr: curr.close()
        #if conn: conn.close()

        return success