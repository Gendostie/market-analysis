#!/usr/bin/python
import finsymbols

from Manager_DB.DbConnection import DBConnection

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'market_analysis'


def get_snp500(db=None):
    """
    Get company with flag is_in_snp500 in db
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return:
    """
    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT name, symbol, last_update_historic
                FROM company WHERE is_in_snp500 = 1"""
    res = db.select_in_db(query)
    db.close_connection()
    return res


def add_company_to_db(symbol, name, db=None):
    """
    add a company to table company
    :param symbol: symbol of company in stock market
    :type symbol: string
    :param name: name of company in stock market
    :type name: string
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: None
    """
    if symbol is None or name is None:
        raise ValueError('Name or symbol is None. name: %(name)s ; symbol: %(symbol)s ' % locals())

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    # Add new company not in table and update name and flag snp500 if already in table
    query = """INSERT INTO company (name, symbol, is_in_snp500) VALUES (UPPER(%(name)s), %(symbol)s, 1)
                ON DUPLICATE KEY UPDATE name = %(name)s, is_in_snp500 = 1"""
    db.modified_db(query, {'name': name, 'symbol': symbol})
    db.close_connection()


def get_company_by_symbol(symbol, db=None):
    """

    :param symbol: symbol of a company we search
    :type symbol: string
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: return tuple of company who correspond to symbol
    :rtype: tuple
    """
    if symbol is None:
        raise ValueError('Symbol is None.')

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT name, symbol, is_in_snp500, last_update_historic
                FROM company WHERE symbol = %(symbol)s"""
    res = db.select_in_db(query, {'symbol': symbol})
    db.close_connection()
    return res


def get_company_by_name(name, db=None):
    """

    :param name: name of a company we search
    :type name: string
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: return tuple of company who correspond to name
    :rtype: tuple
    """
    if name is None:
        raise ValueError('Name is None.')

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT name, symbol, is_in_snp500, last_update_historic
                FROM company WHERE name = %(name)s"""
    res = db.select_in_db(query, {'name': name})
    db.close_connection()
    return res


def update_snp550_to_db(db=None):
    """
    Update data of table company to check if we have new company and remove company not in new list s&p500
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: None
    """
    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    # Set all company in table for to re-init to 0 flag is_in_snp500
    query = """UPDATE company SET is_in_snp500 = 0"""
    db.modified_db(query)

    snp500 = finsymbols.get_sp500_symbols(db)
    # update and add_company of s500
    for company in snp500:
        add_company_to_db(company.get('symbol'), company.get('company'))

    # TODO: call fct to historic data in csv [Gen]
