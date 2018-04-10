""" time_features.py

    Creates a table within the database to map tweetIDs -> date.
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

# For manipulating datetimes
import datetime, pytz


###############################################################################
# Global variables                                                            #
###############################################################################

# Clear and create new feature table
create_sql = """
    DROP TABLE IF EXISTS "features_time" CASCADE;
    CREATE TABLE "features_time" (
        "tweetID" BIGINT NOT NULL,
        "date" TIMESTAMP NOT NULL,
        "period" INT,
        CONSTRAINT features_time_pk PRIMARY KEY ("tweetID")
    ) WITH ( OIDS=FALSE );
"""

# Columns for the new table
cols = ['tweetID', 'date', 'period']

# Select only query we need from the database
select_sql = """
SELECT 
    "tweetID", date
FROM 
    filter_tweets;
"""

# TIME ZONES
EST = pytz.timezone('US/Eastern')
PST = pytz.timezone('US/Pacific')
UTC = pytz.timezone('UTC')

# Beginning
epoch_start_pst = PST.localize(datetime.datetime(2017, 1, 27))
epoch_start_est = epoch_start_pst.astimezone(EST)
epoch_start_utc = epoch_start_pst.astimezone(UTC)

# Ending
epoch_end_pst = PST.localize(datetime.datetime(2017, 1, 28))
epoch_end_est = epoch_end_pst.astimezone(EST)
epoch_end_utc = epoch_end_pst.astimezone(UTC)

# TIME PERIODS
time_period = datetime.timedelta(days=7)


###############################################################################
# Mapping Times/Zones                                                         #
###############################################################################

def create_intervals(start, end, delta):
    """ A function that flexibly create time intervals in relation to an event.
        The event here is one day (time period 0), but any reasonable duration
        will do. 
        
        The time period is dictacted by it's relative distance to the epoch.
        That is, periods before the event are labeled with a negative 
        multiplier to their period. One week before=-1, 4 weeks before=-4, etc.
        
        Args:
            start (datetime): Start of event
            end (datetime): End of event
            delta (timedelta): Duration of time periods outside event.
            
        Returns:
            intervals (list[dict]): A list of intervals w/ start + end times.
    """
    # Hold the intervals
    intervals = []
    add_to = lambda p, s, e: intervals.append({
            'period': p,
            'start': s,
            'end': e
        })

    # Create intervals for 'BEFORE'
    for i in range(-4, 0):
        i_start = start - (abs(i) * delta)
        i_end = start - ((abs(i) - 1) * delta)
        add_to(i, i_start, i_end)

    # Create epoch interval
    add_to(0, start, end)

    # Create intervals for 'AFTER'
    for i in range(1, 5):
        i_start = end + ((i-1) * delta)
        i_end = end + (i * delta)
        add_to(i, i_start, i_end)
        
    return intervals

# Intervals for OUR event
immg_intervals = create_intervals(epoch_start_utc, epoch_end_utc, time_period)


def label_df_date(df, intervals):
    """ Creates a new DataFrame column by mapping row datetimes
        to time periods.
    """
    df = df.assign(period=None)

    # Map intervals to new
    for i in intervals:
        # Format datetimes in an indexable fashion
        start_fmt = i['start'].strftime('%Y-%m-%d %H:00:00')
        end_fmt = i['end'].strftime('%Y-%m-%d %H:00:00')

        # Get the counts
        cnt = len(df[start_fmt: end_fmt])
        print (i['period'], cnt)

        # Assign a time period to the dataframe subset
        df.loc[start_fmt: end_fmt, 'period'] = i['period']
        
    return df



if __name__ == '__main__':
    # Add our utils to path
    sys.path.append('src/utils')
    from df2pg import df2pg
    
    # Load user env
    load_dotenv(find_dotenv())
    
    # Set up database
    database_url = os.environ.get('DATABASE_URL')
    conn = pg.connect(database_url)
    curr = conn.cursor()
    
    try:
        # Clear out database for new feature table
        curr.execute(create_sql)
        conn.commit()
        
        # Read in just the tweetIDs and dates
        date_df = psql.read_sql_query(select_sql, conn, index_col='date')
        
        # Add time periods to dataframe
        date_df = label_df_date(date_df, immg_intervals)
        
        # Reset index for uploading
        date_df.reset_index(inplace=True)
        
        # Write it to database!
        copy_success = df2pg(date_df, cols, curr, 'features_time')
        if copy_success: 
            conn.commit()
        
    except (Exception) as e:
        print (e)
    
    finally:
        if not curr.closed: curr.close()
        if conn: conn.close()
            
    
    print ('\tTime features complete!')
