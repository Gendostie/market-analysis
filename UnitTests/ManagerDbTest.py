#!/usr/bin/python
from os import listdir
from os import path
from Manager_DB.DbConnection import DbConnection


def init_db_mysql_test(host, user, password, database):
    """
    Create database and table for unittest of the program.
    If database exists already, we drop and recreate database.
    :param host: host of db, ex: localhost, 127.0.0.1
    :type host: str
    :param user: user of db
    :type user: str
    :param password:
    :type password: str
    :param database: name of database, can include name table, ex: market_analysis.company
    :type database: str
    :return: connection to db
    :rtype: DbConnection
    """
    # Drop database if exists already
    db = DbConnection(host, user, password, '')  # no database, because we don't know if database exists
    query = """DROP DATABASE IF EXISTS %s""" % ('`' + database + '`')
    db.modified_db(query)
    # Create database
    query = """CREATE DATABASE %s""" % ('`' + database + '`')
    db.modified_db(query)
    db.close_connection()

    # Create another connection, because now we are sure that database exists
    db = DbConnection(host, user, password, database)
    # Create table
    for filename in listdir(path.join('../Data_DB')):
        # Take just filename to finish by extension sql
        if filename.find('sql') != -1:
            f = open(path.join('../Data_DB/' + filename))

            query = ''
            for line in f:
                # exclude comments, line empty and insert/update in table
                if line[0:2] != '/*' and line[0:2] != '--' and line[0:2] != '\n' and line[0:len('ALTER')] != 'ALTER' \
                        and line[0:len('INSERT INTO')] != 'INSERT INTO':
                    query += line
            # remove last ; for new_query empty to end
            # ex: [DROP TABLE IF EXISTS `daily_value`, CREATE TABLE `daily_value`(...), ]
            for new_query in query[:query.rfind(';')].split(';\n'):
                db.modified_db(new_query)
    return db


def drop_db_mysql_test(host, user, password, database, db=None):
    """
    Drop database test
    :param host: host of db, ex: localhost, 127.0.0.1
    :type host: str
    :param user: user of db
    :type user: str
    :param password:
    :type password: str
    :param database: name of database, can include name table, ex: market_analysis.company
    :type database: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: None
    """
    if not db:
        db = DbConnection(host, user, password, '')  # no database if error when create db
    query = """DROP DATABASE IF EXISTS %s""" % ('`' + database + '`')
    db.modified_db(query)
    db.close_connection()
