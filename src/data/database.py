import os
import logging
import click
from dotenv import load_dotenv, find_dotenv
import psycopg2 as pg

def read_sql(f):
    cmd = f.read().strip()
    cmds = [c for c in cmd.replace('\n', '').split(';')]
    valid_cmds = [c for c in cmds if c != '']
    return valid_cmds

###############################################################################
# Database CLI Wrapper                                                        #
###############################################################################

@click.command()
@click.argument('f', type=click.File('r'))
@click.argument('db_url', type=str, envvar='DATABASE_URL')
def main(f, db_url):
    """Executes one or more SQL commands on a remote PostgreSQL database.

    Function includes a Python logger, which will be outputing the information of each command. This is used instead of a return value for our Makefile.
    
    Args:
        url (str): Database URL formatted for Python's psycopg2 (postgres://user:password@host:port/database)
        sql_cmds (tuple[str]): A tuple, containing one or more SQL statements as strings.

    Returns:
        None: But, the function outputs to `report/pipeline.database.log`.
    """
    # Logging
    logger = logging.getLogger(__name__)
    log_db = logger.getChild('database')

    # Create a database connection pointer
    conn = None
    logger.info('creating database')
    log_db.info('attemping to connect to database')

    try:
        # Connect to the PostgreSQL server
        conn = pg.connect(db_url)
        cur = conn.cursor()
        log_db.info('connected! Executing SQL commands')
        click.echo(click.style('\tconnected! executing commands...', fg='green'))

        # Execute sql commands
        sql_cmds = read_sql(f)
        for sql in sql_cmds:
            cur.execute(sql)
            # Log the SQL command to file.
            log_db.info('executed: ' + sql)

        # Close communication, close connection to SQL server.
        cur.close()
        conn.commit()
    
    except (Exception, pg.DatabaseError) as error:
        log_db.error('error while executing SQL{}'.format(error))
        click.echo(click.style('Error! {}'.format(error), fg='red'))
    
    finally:
        if conn is not None:
            log_db.info('closing PostgreSQL connection')
            click.echo(click.style('\tclosing PostgreSQL database connection.', fg='green'))
            conn.close()


if __name__ == '__main__':
    # Configure logging
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO,  
                    format=log_fmt, datefmt='%H:%M:%S',
                    filename='reports/pipeline.database.log', filemode='a')

    # Environmental variables
    load_dotenv(find_dotenv())
    # Run script
    main()
