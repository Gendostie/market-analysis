#!/usr/bin/python
import finsymbols
from os import path

from Manager_DB import ManagerCompany
from Manager_DB.DbConnection import DBConnection

# TODO : Add config
HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'market_analysis'
PATH_DATA_DB = '../Data_DB/'


def insert_company_snp500():
    """Insert in the db the name and the symbol of every S&P500's company."""
    snp500 = finsymbols.get_sp500_symbols()

    row_affected = 0
    for company in snp500:
        row_affected += ManagerCompany.add_company_to_db(company.get('symbol'), company.get('company'))
    print("Number of rows affected: %s" % row_affected)


def create_db_mysql():
    """
    Usage: In the very beginning only or if any changes must be made in the database's tables.
    Drop the current database.
    Create a new database with its tables. Use
    If database exists already, we drop and recreate database and its tables.
    :return: None
    """
    # Drop the database if it already exists
    db = DBConnection(HOST, USER, PASSWORD, '')  # no database, because we don't know if database exists
    query = """DROP DATABASE IF EXISTS %s""" % ('`' + DATABASE + '`')
    print('Number of tables removed: %s' % db.modified_db(query))

    # Create a new database
    query = """CREATE DATABASE %s""" % ('`' + DATABASE + '`')
    print('Creation of database: %s' % db.modified_db(query))
    db.close_connection()

    # Create another connection, because now we are sure that database exists
    db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    # Create tables
    # TODO : Add config
    list_file = ['company', 'daily_value', 'historic_value', 'portfolio', 'simulation', 'transaction']
    for filename in list_file:
        # Take just filename to finish by extension sql
        f = open(path.join(PATH_DATA_DB + DATABASE + '_' + filename + '.sql'))

        query = ''
        for line in f:
            # exclude comments, line empty
            if line[0:2] != '/*' and line[0:2] != '--' and line[0:2] != '\n':
                query += line
        row_affected = 0
        # remove last ; for new_query empty to end
        # ex: [DROP TABLE IF EXISTS `daily_value`, CREATE TABLE `daily_value`(...), ]
        for new_query in query[:query.rfind(';')].split(';\n'):
            row_affected += db.modified_db(new_query)
        print('Number of rows affected for table %s: %s' % (filename, row_affected))
