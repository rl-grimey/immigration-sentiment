# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv


def get_twitter_files(input_filepath):
    """ Returns a list of all .csv files in the input directory.
        :param: input_filepath - File path to directory containing raw twitter scrapes.
        :returns: List of .csv filepaths for importing.
    """
    print ('\tGathering file names...')
    filtered_files = []

    try:
        files = os.listdir(working_dir)

        # Filter log files keeping only csv/non-hidden files
        filtered_files = [f for f in files if \
            (f.endswith('.csv') and not f.startswith('.'))]

        # Create file paths by combining it with our passed directory
        filtered_files = [os.path.join(input_filepath, f) for f in filtered_files]

    except Exception as error:
        print ('\tCould not find directory!')
        print ('\tError: ', error)
    
    finally:
        return filtered_files




@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
