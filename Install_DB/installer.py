import os
import initialize_db as init_sql
import update_manager as um
import configparser
from time import localtime, strftime


def print_message(message):
    """Print a message on the command line. Useful for debugging."""
    line = '--------------- '
    print(line + message + '\n')


# TODO : Check for requirements, check for config.ini. Check that the database exists too?
# Fetch the configuration file
config = configparser.ConfigParser()
config.read('../config.ini')

# Installation (or re-installation) of the database if required
if config['installer'].getboolean('INSTALL_DB'):
    print_message('Installing the database')
    init_sql.create_db_mysql()
    # init_sql.insert_company_snp500()

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

# Update the configuration file so, next time, it won't try to update what was already done.
# Also, next time, it won't drop the database or try to update the historical data (which rarely changes)
# Note: The months begin with 0. So 0 = January and 11 = December
# config['installer']['install_fetch_histo'] = "False"
# config['installer']['install_set_histo'] = "False"
config['installer']['install_db'] = "False"


if config['installer'].getboolean('INSTALL_FETCH_DAILY'):
    config['daily']['DAY_MIN'] = strftime("%d", localtime())
    config['daily']['MONTH_MIN'] = str(localtime().tm_mon - 1)
    config['daily']['YEAR_MIN'] = strftime("%Y", localtime())

if config['installer'].getboolean('INSTALL_FETCH_DIV'):
    config['dividend']['DAY_MIN'] = strftime("%d", localtime())
    config['dividend']['MONTH_MIN'] = str(localtime().tm_mon - 1)
    config['dividend']['YEAR_MIN'] = strftime("%Y", localtime())

with open('../config.ini', 'w') as configfile:
    config.write(configfile)
