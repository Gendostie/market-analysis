#!/usr/bin/python
import pymysql


class DbConnection:
    """
    Create connection with db MySql and give possibility to execute query sql
    """
    def __init__(self, host, user, password, database):
        """
        Create connection to db MySql
        :param host: host of db, ex: localhost, 127.0.0.1
        :type host: str
        :param user: user of db
        :type user: str
        :param password:
        :type password: str
        :param database: name of database, can include name table, ex: market_analysis.company
        :type database: str
        """
        try:
            self.__connection = pymysql.connect(host=host, user=user, passwd=password, db=database)
            self.__cursor = self.__connection.cursor()
        except pymysql.Error as e:
            print('Error connection: ', e, 
                  '\nwith parameters %(host)s, %(user)s, %(password)s, %(database)s' % locals())
            raise ValueError('Error in call of the query: ', e,
                             '\nwith parameters: \"%(host)s, %(user)s, %(password)s, %(database)s\"' % locals())

    def close_connection(self):
        """
        Close connection to db MySql
        :return: None
        """
        if self.__cursor is not None:
            self.__cursor.close()
        if self.__connection is not None:
            self.__connection.close()

    def select_in_db(self, query, params=None):
        """
        Function to call query select to db
        :param query: query sql
        :type query: str
        :param params: parameter to put in query, ex: "WHERE id = %s" or "WHERE id = %(id)s",  params = {id: 1}
        :type params: dict
        :return: result of query select
        :rtype tuple(tuple)
        """
        try:
            self.__cursor.execute(query, params)
            return self.__cursor.fetchall()
        except pymysql.Error as e:
            print('Error in call of the query: ', e, '\nwith parameters %(query)s, %(params)s' % locals())
            raise ValueError('Error in call of the query: ', e,
                             '\nwith parameters: \"%(query)s\" ; \"%(params)s\"' % locals())

    def modified_db(self, query, params=None):
        """
        Function to call query who modified data in db. INSERT, UPDATE and DELETE
        :param query: query sql
        :type query: str
        :param params: parameter to put in query, ex: "WHERE id = %s" or "WHERE id = %(id)s",  params = {id: 1}
        :type params: dict
        :return: Number row affected
        :rtype: int
        """
        try:
            self.__cursor.execute(query, params)
            self.__connection.commit()
            return self.__cursor.rowcount
        except pymysql.Error as e:
            self.__connection.rollback()
            print('Error in call of the query: ', e, '\nwith parameters %(query)s, %(params)s' % locals())
            raise ValueError('Error in call of the query: ', e,
                             '\nwith parameters: \"%(query)s\" ; \"%(params)s\"' % locals())
