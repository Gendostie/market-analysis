#!/usr/bin/python
import os
import Install_DB.initialize_db as init_sql
import Install_DB.initialize_data as init_data

LINE = '--------------- '

PATH = os.getcwd()
DIR_NAME = '/../SNP500/'
DIR_PATH = PATH + DIR_NAME

INSTALL_DB = False
INSTALL_ALL_DATA = True
INSTALL_HISTO = False
INSTALL_DAILY = False
DEBUG = True


def print_message(message):
    """Print a message on the command line. Used for debugging."""
    print(LINE + message + '\n')


# TODO : Add GetConfigParams

# Installation (or re-installation) of the database if required
# TODO : Don't drop all the tables (like daily...)
if INSTALL_DB:
    print_message('Installing the database')
    init_sql.create_db_mysql()
    init_sql.insert_company_snp500()

# Make directory if it doesn't exist
if not os.path.exists(DIR_PATH):
    print_message('Creating the directory SNP500 for the CSVs')
    os.makedirs(DIR_PATH)

# TODO : Add a comment
if INSTALL_ALL_DATA:
    print_message('Fetching all the CSVs')
    init_data.get_all_csv()
    # TODO : Add the CSVs that we can't fetch
    print_message('Updating the database with all the CSVs')
    init_data.update_all_with_csv()
    # TODO : SNP500 as param...
elif INSTALL_HISTO:
    print_message('Updating the historic database with the CSVs')
elif INSTALL_DAILY:
    print_message('Updating the daily database with the CSVs')
