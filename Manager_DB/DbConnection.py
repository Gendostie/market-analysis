#!/usr/bin/python
import MySQLdb


class DBConnection:
    """
    Create connection with db MySql and give possibility to execute query sql
    """
    __connection = None
    __cursor = None

    __host = None
    __user = None
    __password = None
    __database = None

    def __init__(self, host, user, password, database):
        """
        Create connection to db MySql
        :param host:
        :type host: str
        :param user:
        :type user: str
        :param password:
        :type password: str
        :param database:
        :type database: str
        """
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

        try:
            self.__connection = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
            self.__cursor = self.__connection.cursor()
        except MySQLdb.Error as e:
            print 'Error connection: ', e.message, \
                '\nwith parameters %(host)s, %(user)s, %(password)s, %(database)s' % locals()
            raise ValueError('Error in call of the query: ', e.message,
                             '\nwith parameters %(host)s, %(user)s, %(password)s, %(database)s' % locals())

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
        except MySQLdb.Error as e:
            print 'Error in call of the query: ', e, \
                '\nwith parameters %(query)s, %(params)s' % locals()
            raise ValueError('Error in call of the query: ', e,
                             '\nwith parameters %(query)s ; %(params)s' % locals())

    def modified_db(self, query, params=None):
        """
        Function to call query who modified data in db. INSERT, UPDATE and DELETE
        :param query: query sql
        :type query: str
        :param params: parameter to put in query, ex: "WHERE id = %s" or "WHERE id = %(id)s",  params = {id: 1}
        :type params: dict
        :return: None
        """
        try:
            self.__cursor.execute(query, params)
            self.__connection.commit()
        except MySQLdb.Error as e:
            self.__connection.rollback()
            print 'Error in call of the query: ', e, \
                '\nwith parameters %(query)s, %(params)s' % locals()
            raise ValueError('Error in call of the query: ', e,
                             '\nwith parameters %(query)s ; %(params)s' % locals())
