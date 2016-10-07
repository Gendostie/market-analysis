#!/usr/bin/python
import finsymbols
from os import listdir
from os import path

from Manager_DB import ManagerCompany
from Manager_DB.DbConnection import DBConnection

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'market_analysis'


def insert_company_snp500():
    """
    Insert company s&p500 in table company
    :return: None
    """
    snp500 = finsymbols.get_sp500_symbols()

    for company in snp500:
        ManagerCompany.add_company_to_db(company.get('symbol'), company.get('company'))


def init_update_db_mysql():
    """
    Create database and table for use the program.
    If database exists already, we drop and recreate database and its tables.
    :return: None
    """
    # Drop database if exists already
    db = DBConnection(HOST, USER, PASSWORD, '')  # no database, because we don<t know if database exists
    query = """DROP DATABASE IF EXISTS %s""" % ('`' + DATABASE + '`')
    db.modified_db(query)
    # Create database
    query = """CREATE DATABASE %s""" % ('`' + DATABASE + '`')
    db.modified_db(query)
    db.close_connection()

    # Create another connection, because now we are sure that database exists
    db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    # Create table
    for filename in listdir(path.join('Data_DB')):
        # Take just filename to finish by extension sql
        if filename.find('sql') != -1:
            f = open(path.join('Data_DB/' + filename))

            query = ''
            for line in f:
                if line[0:2] != '/*' and line[0:2] != '--' and line[0:2] != '\n':
                    query += line
            # remove last ; for new_query empty to end
            # ex: [DROP TABLE IF EXISTS `daily_value`, CREATE TABLE `daily_value`(...), ]
            for new_query in query[:query.rfind(';')].split(';\n'):
                db.modified_db(new_query)
