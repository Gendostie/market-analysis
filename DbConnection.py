#!/usr/bin/python
import mysql.connector


class DBConnection:
    __connection = None
    __cursor = None

    __host = None
    __user = None
    __password = None
    __database = None

    def __init__(self, host, user, password, database):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

        try:
            self.__connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
            self.__cursor = self.__connection.cursor()
        except mysql.connector.Error as e:
            print 'Error connection: ', e.message, \
                '\nwith parameters %(host)s, %(user)s, %(password)s, %(database)s' % locals()
            raise ValueError('Error in call of the query: ', e.message,
                             '\nwith parameters %(host)s, %(user)s, %(password)s, %(database)s' % locals())

    def close_connection(self):
        if self.__cursor is not None:
            self.__cursor.close()
        if self.__connection is not None:
            self.__connection.close()

    def select_in_db(self, query, params=None):
        """
        Function to call query select to db
        :param query: query sql
        :type query: string
        :param params: parameter to put in query, ex: "WHERE id = %s" or "WHERE id = %(id)s",  params = {id: 1}
        :type params: dict
        :return: result of query select
        :rtype tuple
        """
        try:
            self.__cursor.execute(query, params)
            return self.__cursor.fetchall()
        except mysql.connector.Error as e:
            print 'Error in call of the query: ', e.message, \
                '\nwith parameters %(query)s, %(params)s' % locals()
            raise ValueError('Error in call of the query: ', e.message,
                             '\nwith parameters %(query)s, %(params)s' % locals())

    def modified_db(self, query, params=None):
        """
        Function to call query who modified data in db. INSERT, UPDATE and DELETE
        :param query: query sql
        :type query: string
        :param params: parameter to put in query, ex: "WHERE id = %s" or "WHERE id = %(id)s",  params = {id: 1}
        :type params: dict
        :return: None
        """
        try:
            self.__cursor.execute(query, params)
            self.__cursor.commit()
        except mysql.connector.Error as e:
            self.close_connection()
            print 'Error in call of the query: ', e.message, \
                '\nwith parameters %(query)s, %(params)s' % locals()
            raise ValueError('Error in call of the query: ', e.message,
                             '\nwith parameters %(query)s, %(params)s' % locals())

