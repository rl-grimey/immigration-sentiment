import os

def main():
    """ Function to create a per-user environment file for analysis.
        This function takes no parameters and instead relies on user input.
        Includes a confirmation 
    """
    # Default values
    default_user = os.environ.get('USER')
    default_db = 'immigrationsentiment'
    default_host = 'localhost'
    default_port = 5432
    default_data = '/data/'

    # User variables, loop until we get the right params.
    user_approved = False
    while not user_approved:
        db = input('Enter a database (DB) [{}]: '.format(default_db)) or default_db
        user = input('Enter username for DB [{}]: '.format(default_user)) or default_user
        passw = input('Enter pass for DB [hawkID password]: ')
        host = input('Enter DB host [{}]: '.format(default_host)) or default_host
        port = input('Enter DB port [{}]: '.format(default_port)) or default_port

        # Check with the user if the values are correct
        approved = input('\n---------------\nDatabase: {}\nUsername: {}\nHost: {}\nPort: {}\n\nAccept? [y/N]: '.format(db, user, passw, host, port))
        if approved == 'y':
            user_approved = True
    
    # .env file
    database_url = 'postgres://{}:{}@{}:{}/{}'.format(user, passw, host, port, db)
    import_url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user, passw, host, port, db)
    env = """
    # DO NOT COMMIT THIS TO GIT

    USER={}
    PASS={}
    DATA_DIR={}
    DATABASE={}
    DATABASE_URL={}
    IMPORT_URL={}
    """.format(user, passw, default_data, db, database_url, import_url)

    # Check for .env file, don't overwrite
    if not os.path.isfile('.env'):
        with open('.env', 'w') as envfile:
            envfile.writelines(env)
        envfile.close()

if __name__ == '__main__':
    main()
