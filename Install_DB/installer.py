#!/usr/bin/python
import os
import Install_DB.initialize_db as init_sql
import Install_DB.update_manager as um
import configparser


def print_message(message):
    """Print a message on the command line. Useful for debugging."""
    LINE = '--------------- '
    print(LINE + message + '\n')


# TODO : Check for requirements, check for config.ini
# Fetch the configuration file
config = configparser.ConfigParser()
config.read('../config.ini')

# Installation (or re-installation) of the database if required
# TODO : Don't drop all the tables (like daily...)
if config['installer'].getboolean('INSTALL_DB'):
    print_message('Installing the database')
    init_sql.create_db_mysql()
    init_sql.insert_company_snp500()

# Make directory if it doesn't exist
if not os.path.exists(config['path']['PATH_SNP500']):
    print_message('Creating the directory SNP500 for the CSVs')
    os.makedirs(config['path']['PATH_SNP500'])

print_message('Fetching all the CSVs')
um.get_csv(config['installer'].getboolean('INSTALL_FETCH_HISTO'),
           config['installer'].getboolean('INSTALL_FETCH_DAILY'),
           config['installer'].getboolean('INSTALL_FETCH_DIV'))

# TODO : Add the CSVs that we can't fetch
print_message('Updating the database with all the CSVs')
um.update_with_csv(config['installer'].getboolean('INSTALL_SET_HISTO'),
                   config['installer'].getboolean('INSTALL_SET_DAILY'),
                   config['installer'].getboolean('INSTALL_SET_DIV'))
