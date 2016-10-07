#!/usr/bin/python
from Manager_DB.DbConnection import DBConnection

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'market_analysis'


def get_id_portfolio(name, db=None):
    """
    Get name of portfolio as name of portfolio
    :param name: name of portfolio
    :type name: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: result in tuple of tuple
    :rtype: tuple(tuple)
    """
    if not name:
        raise ValueError('Name portfolio is None.')

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_portfolio FROM portfolio WHERE name = %(name)s"""
    return db.select_in_db(query, {'name': name})


def get_name_portfolio_name(id_portfolio, db=None):
    """
    Get name of portfolio as id of portfolio
    :param id_portfolio: id of portfolio
    :type id_portfolio: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: result in tuple of tuple
    :rtype: tuple(tuple)
    """
    if not id_portfolio:
        raise ValueError('ID portfolio is None.')

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT name FROM portfolio WHERE id_portfolio = %(id)s"""
    return db.select_in_db(query, {'id': id_portfolio})


def get_transaction_portfolio(id_portfolio, symbol_company=None, db=None):
    """
    Get all transaction of portfolio and if we want of a company
    :param id_portfolio: id of portfolio
    :type id_portfolio: int
    :param symbol_company: symbol of company in stock market
    :type symbol_company: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: result in tuple of tuple
    :rtype: tuple(tuple)
    """
    if not id_portfolio:
        raise ValueError('ID portfolio is None.')

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_transaction, id_symbol, quantity, value_current, transaction_date, id_simulation
                FROM transaction WHERE id_portfolio = %(id_portfolio)s"""
    params = {'id_portfolio': id_portfolio}
    if symbol_company:
        query += "AND id_symbol = %(id_symbol)s"
        params['symbol_company'] = symbol_company
    return db.select_in_db(query, params)


def get_simulation_portfolio(id_portfolio, db=None):
    """
    Get all simulation of portfolio
    :param id_portfolio: id of portfolio
    :type id_portfolio: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: result in tuple of tuple
    :rtype: tuple(tuple)
    """
    if not id_portfolio:
        raise ValueError('ID portfolio is None.')

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_simulation, parameters, results
                FROM simulation WHERE id_portfolio = %(id_portfolio)s"""
    params = {'id_portfolio': id_portfolio}
    return db.select_in_db(query, params)


def create_portfolio(name=None, db=None):
    """
    Create new portfolio
    :param name:
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: id of portfolio
    :rtype int
    """
    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    if not name:
        query = """SELECT (CASE COUNT(id_portfolio) WHEN 0 THEN 1 ELSE COUNT(id_portfolio)+1 END) AS new_id
                    FROM portfolio"""
        res = db.select_in_db(query)
        name = 'new_portfolio' + str(res[0][0])

    query = """INSERT INTO portfolio (name) VALUES (%(name)s)"""
    db.modified_db(query, {'name': name})
    # get id portfolio
    query = """SELECT id_portfolio FROM portfolio WHERE name = %(name)s"""
    return db.select_in_db(query, {'name': name})[0][0] # if we have more one with the same name, we take the first


def insert_transaction_to_db(id_portfolio, symbol_company, quantity, value_current, transaction_date,
                             id_simulation=None, db=None):
    """
    Insert transaction link to portfolio
    :param id_portfolio: id of portfolio
    :type id_portfolio: int
    :param symbol_company: symbol of a company
    :type symbol_company: str
    :param quantity:
    :type quantity: int
    :param value_current:
    :type value_current: float
    :param transaction_date:
    :type transaction_date: datetime
    :param id_simulation: if transaction is during simulation
    :type id_simulation: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: number row affected
    :rtype: int
    """
    if not id_portfolio:
        raise ValueError("Need to id_portfolio valid to create transaction. id_portfolio = %s" % id_portfolio)
    if not symbol_company:
        raise ValueError("Need to symbol_company valid to create transaction. symbol_company = %s" % symbol_company)

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    query = """INSERT INTO transaction (id_portfolio, id_symbol, quantity, value_current,
                                                        transaction_date, id_simulation)
                VALUES (%(id_portfolio)s, %(symbol_company)s, %(quantity)s, %(value_current)s, %(transaction_date)s,
                        %(id_simulation)s)
                ON DUPLICATE KEY UPDATE id_symbol = %(symbol_company)s, quantity = %(quantity)s,
                                        value_current = %(value_current)s, transaction_date = %(transaction_date)s,
                                        id_simulation = %(id_simulation)s)"""
    params = {'id_portfolio': id_portfolio, 'symbol_company': symbol_company, 'quantity': quantity,
              'value_current': value_current, 'transaction_date': transaction_date, 'id_simulation': id_simulation}
    return db.modified_db(query, params)


# TODO: to complete
def start_simulation(dict_params, id_portfolio=None, db=None):
    """
    As parameter giving, a simulation of a portfolio is doing
    :param dict_params:
    :type dict_params: dict{string}
    :param id_portfolio: id of portfolio
    :type id_portfolio: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return:
    """
    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    if not id_portfolio:
        id_portfolio = create_portfolio()

    print('Simulation start')


def get_info_simulation(id_simulation, db=None):
    """
    Get information of simulation as id of simulation
    :param id_simulation: id of simulation
    :type id_simulation: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: information on simulation
    :rtype: tuple(tuple())
    """
    if not id_simulation:
        raise ValueError('ID simulation is None.')

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_portfolio, parameters, results
                FROM simulation WHERE id_simulation = %(id_simulation)s"""
    return db.select_in_db(query, {'id_simulation': id_simulation})


def get_transaction_simulation(id_simulation, db=None):
    """
    Get transaction of simulation as id of simulation
    :param id_simulation: id of simulation
    :type id_simulation: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: transaction of simulation
    :rtype: tuple(tuple())
    """
    if not id_simulation:
        raise ValueError('ID simulation is None.')

    if not db:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_transaction, id_portfolio, id_symbol, quantity, value_current, transaction_date
                FROM "transaction" WHERE id_simulation = %(id_simulation)s"""
    return db.select_in_db(query, {'id_simulation': id_simulation})
