#!/usr/bin/python
from QT.Singleton import get_snp500
from os import path
import json
import configparser
from Manager_DB import ManagerCompany
from Manager_DB.DbConnection import DbConnection


def insert_company_snp500():
    """Insert in the db the name and the symbol of every S&P500's company."""
    # TODO: Add comment
    snp500 = get_snp500()

    row_affected = 0
    for company in snp500:
        row_affected += ManagerCompany.add_company_to_db(company.get('symbol'), company.get('company'))
    print("Number of rows affected: %s" % row_affected)


def create_db_mysql():
    # TODO  Clean comment
    """
    Usage: In the very beginning only or if any changes must be made in the database's tables.
    Drop the current database.
    Create a new database with its tables. Use
    If database exists already, we drop and recreate database and its tables.
    :return: None
    """
    # Fetch the configuration file and some variables
    config = configparser.ConfigParser()
    config.read('../config.ini')

    host = config['database']['HOST']
    user = config['database']['USER']
    password = config['database']['PASSWORD']
    database = config['database']['DATABASE']
    path_data_db = config['path']['PATH_DATA_DB']

    # Drop the database if it already exists
    db = DbConnection(host, user, password, '')  # no database, because we don't know if database exists
    query = """DROP DATABASE IF EXISTS %s""" % ('`' + database + '`')
    print('Number of tables removed: %s' % db.modified_db(query))

    # Create a new database
    query = """CREATE DATABASE %s""" % ('`' + database + '`')
    print('Creation of database: %s' % db.modified_db(query))
    db.close_connection()

    # Create another connection, because now we are sure that database exists
    db = DbConnection(host, user, password, database)

    # Create tables
    list_tables_name = json.loads(config.get('list', 'TABLES_NAME'))
    for table in list_tables_name:
        # Take just filename to finish by extension sql
        f = open(path.join(path_data_db + database + '_' + table + '.sql'))

        query = ''
        for line in f:
            # exclude comments, line empty
            if line[0:2] != '/*' and line[0:2] != '--' and line[0:2] != '\n' \
                    and line[0:len('DROP TABLE')] != 'DROP TABLE':
                query += line
        row_affected = 0
        # remove last ; for new_query empty to end
        # ex: [DROP TABLE IF EXISTS `daily_value`, CREATE TABLE `daily_value`(...), ]
        for new_query in query[:query.rfind(';')].split(';\n'):
            row_affected += db.modified_db(new_query)
        print('Number of rows affected for table %s: %s' % (table, row_affected))
