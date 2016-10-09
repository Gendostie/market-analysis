#!/usr/bin/python
import os
import Install_DB.initialize_db as idb
import Install_DB.initialize_data as ida

LINE = '--------------- '

PATH = os.getcwd()
DIR_NAME = '/../SNP500/'
DIR_PATH = PATH + DIR_NAME

DEBUG = True


def print_message(message):
    print(LINE + message + '\n')

# TODO : Add a comment
print_message('Installing the database')
idb.init_update_db_mysql()

# TODO : Add a comment
print_message('Loading the name of each company')
idb.insert_company_snp500()

if not DEBUG:
    # TODO : Make directory if it doesn't exist
    if not os.path.exists(DIR_PATH):
        print_message('Creating the directory SNP500 for the CSVs')
        os.makedirs(DIR_PATH)

    # TODO : Use the script GetData
    print_message('Fetching the CSVs from MorningStar')
    ida.get_all_csv()

# TODO : Use the script CleanData
print_message('Updating the database with the CSVs')
ida.update_bd_with_csv()
