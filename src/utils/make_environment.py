import os

def create_clinput(prompt, default_val, *args):
    """Function to programatically create a user input prompt. Includes default value as a fallback.

    Args:
        prompt (str): Prompt user is presented with. Should include `{}` for formattting default_val.
        default_val (str/int): Default value used as a fallback for prompt.
        *args (str/int): Additional arguments to format prompt, used for displaying to user for approval.
    
    Returns:
        user_input (str): Input from the user, OR default value.
    """
    user_input = input(prompt.format(default_val, *args)) or default_val
    return user_input

def main():
    """ Function to gather user information and write it to file. Includes a confirmation prompt to user can review stored information.
    
        Args:
            None: This function takes no parameters and instead relies on user input from the command line.
        
        Returns:
            .env (file): .env file 
    """
    # Default values
    default_user = os.environ.get('USER')
    default_db = 'immigrationsentiment'
    default_host = 'localhost'
    default_port = 5432
    default_data = '/data/backed_up/'

    approval_str = """
-------------------------------------------------------------------------------
Database: {}
Username: {}
Host: {}
Port: {}
Data Directory: {}

Accept? [y/N]: """

    # User variables, loop until we get the right params.
    user_approved = False
    while not user_approved:
        
        # Separate input from other CLI stuff
        print ('-------------------------------------------------------------------------------')

        # Get user values
        db = create_clinput('Enter a database (DB) [{}]: ', default_db)
        user = create_clinput('Enter username for DB [{}]: ', default_user)
        passw = create_clinput('Enter password for DB [hawkID password]:{} ', '')
        host = create_clinput('Enter DB host [{}]: ', default_host)
        port = create_clinput('Enter DB port [{}]: ', default_port)
        data_dir = create_clinput('Enter directory of raw data [{}]: ', default_data)

        # Check with the user if the values are correct
        approved = create_clinput(approval_str, db, user, host, port, data_dir)
        if approved == 'y':
            user_approved = True
    
    # Used for interacting with our database through Python's psycopg2
    database_url = 'postgres://{}:{}@{}:{}/{}'.format(user, passw, host, port, db)
    # Used for interacting with our database through SQLAlchemy
    import_url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user, passw, host, port, db)
    # Format our environment file.
    env = """
# DO NOT COMMIT THIS TO GIT

NLTK_DATA=models/nltk
USER={}
PASS={}
DATA_DIR={}
DATABASE={}
DATABASE_URL={}
IMPORT_URL={}
""".format(user, passw, data_dir, db, database_url, import_url)

    # Check for .env file, don't overwrite if we have already created it.
    if not os.path.isfile('.env'):
        with open('.env', 'w') as envfile:
            envfile.writelines(env)
        envfile.close()

if __name__ == '__main__':
    main()