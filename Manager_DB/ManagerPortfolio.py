#!/usr/bin/python
import sys
from DbConnection import DbConnection

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
    :type db: DbConnection
    :return: result in list of dict
    :rtype: list[dict]
    """
    if not name:
        raise ValueError('Name portfolio is None.')

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_portfolio FROM portfolio WHERE name = %(name)s"""
    res = db.select_in_db(query, {'name': name})
    return_value = []
    for id_portfolio in res:
        return_value.append({'id_portfolio': id_portfolio})
    return return_value


def get_all_portfolio_info(db=None):
    """
    Get all portfolio with name and id
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: list[dict]
    """
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_portfolio, name FROM portfolio"""
    res = db.select_in_db(query)
    return_value = []
    for id_portfolio, name in res:
        return_value.append({'id_portfolio': id_portfolio, 'name': name})
    return return_value


def get_name_portfolio_name(id_portfolio, db=None):
    """
    Get name of portfolio as id of portfolio
    :param id_portfolio: id of portfolio
    :type id_portfolio: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: result in list of dict
    :rtype: list[dict]
    """
    if not id_portfolio:
        raise ValueError('ID portfolio is None.')

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT name FROM portfolio WHERE id_portfolio = %(id)s"""
    res = db.select_in_db(query, {'id': id_portfolio})
    return_value = []
    for name in res:
        return_value.append({'name': name})
    return return_value


def get_transaction_portfolio(id_portfolio, symbol_company=None, db=None):
    """
    Get all transaction of portfolio and if we want of a company
    :param id_portfolio: id of portfolio
    :type id_portfolio: int
    :param symbol_company: symbol of company in stock market
    :type symbol_company: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: result in list of dict
    :rtype: list[dict]
    """
    if not id_portfolio:
        raise ValueError('ID portfolio is None.')

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_transaction, id_symbol, quantity, value_current, transaction_date, id_simulation
                FROM transaction WHERE id_portfolio = %(id_portfolio)s"""
    params = {'id_portfolio': id_portfolio}
    if symbol_company:
        query += "AND id_symbol = %(id_symbol)s"
        params['symbol_company'] = symbol_company
    res = db.select_in_db(query, params)
    return_value = []
    for id_transaction, id_symbol, quantity, value_current, transaction_date, id_simulation in res:
        return_value.append({'id_transaction': id_transaction, 'id_symbol': id_symbol, 'quantity': quantity,
                             'value_current': value_current, 'transaction_date': transaction_date,
                             'id_simulation': id_simulation})
    return return_value


def get_simulation_portfolio(id_portfolio, db=None):
    """
    Get all simulation of portfolio
    :param id_portfolio: id of portfolio
    :type id_portfolio: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: result in list of dict
    :rtype: list[dict]
    """
    if not id_portfolio:
        raise ValueError('ID portfolio is None.')

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_simulation, parameters, results
                FROM simulation WHERE id_portfolio = %(id_portfolio)s"""
    params = {'id_portfolio': id_portfolio}
    res = db.select_in_db(query, params)
    return_value = []
    for id_simulation, parameters, results in res:
        return_value.append({'id_simulation': id_simulation, 'parameters': parameters, 'results': results})
    return return_value


def create_portfolio(name=None, db=None):
    """
    Create new portfolio
    :param name: name of portfolio
    :type name: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: id of portfolio
    :rtype int
    """
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    if not name:
        query = """SELECT (CASE COUNT(id_portfolio) WHEN 0 THEN 1 ELSE COUNT(id_portfolio)+1 END) AS new_id
                    FROM portfolio"""
        res = db.select_in_db(query)
        name = 'new_portfolio' + str(res[0][0])

    query = """INSERT INTO portfolio (name) VALUES (%(name)s) ON DUPLICATE KEY UPDATE name = name"""
    db.modified_db(query, {'name': name})
    # get id portfolio
    return get_id_portfolio(name, db)


def add_companies_to_portfolio(portfolio, list_company, db=None):
    """
    Add list of company to portfolio
    :param portfolio: id or name of portfolio
    :type portfolio: int|string
    :param list_company: list contains symbol of company
    :type list_company: list[str]
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: nb added company to portfolio
    :rtype: int
    """
    if not db or not isinstance(db, DbConnection):
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    # check if id or name of portfolio, if name => get id
    if isinstance(portfolio, str):
        if not portfolio.isdigit():
            id_portfolio = get_id_portfolio(portfolio)
            portfolio = id_portfolio[0].get('id_portfolio')[0]
    # check if portfolio number is valid
    if not portfolio:
        raise ValueError("Need to portfolio valid to add company to portfolio. portfolio = %s" % portfolio)

    # add each company to portfolio
    query = """INSERT INTO company_portfolio (id_portfolio, symbol_company, is_activate_in_portfolio)
                VALUES (%(id_portfolio)s, %(symbol_company)s, 1) ON DUPLICATE KEY UPDATE is_activate_in_portfolio = 1"""
    nb_company_add = 0
    for company in list_company:
        params = {'id_portfolio': portfolio, 'symbol_company': company}
        nb_company_add += db.modified_db(query, params)
    return nb_company_add


def get_companies_to_portfolio(portfolio, db=None):
    """
    Get all company associate to a portfolio
    :param portfolio: id or name of portfolio
    :type portfolio: int|string
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: list company name  and symbol
    :rtype: list[dict]
    """
    if not db or not isinstance(db, DbConnection):
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    # check if id or name of portfolio, if name => get id
    if isinstance(portfolio, str):
        if not portfolio.isdigit():
            id_portfolio = get_id_portfolio(portfolio)
            portfolio = id_portfolio[0].get('id_portfolio')[0]
    # check if portfolio number is valid
    if not portfolio:
        raise ValueError("Need to portfolio valid to add company to portfolio. portfolio = %s" % portfolio)

    query = """SELECT c.name, cp.symbol_company
                FROM company_portfolio cp JOIN company c ON c.symbol = cp.symbol_company
                WHERE cp.id_portfolio = %(portfolio)s AND cp.is_activate_in_portfolio = 1"""
    res = db.select_in_db(query, {'portfolio': portfolio})
    return_value = []
    for name, symbol in res:
        return_value.append({'name': name, 'symbol': symbol})
    return return_value


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
    :type db: DbConnection
    :return: number row affected
    :rtype: int
    """
    if not id_portfolio:
        raise ValueError("Need to id_portfolio valid to create transaction. id_portfolio = %s" % id_portfolio)
    if not symbol_company:
        raise ValueError("Need to symbol_company valid to create transaction. symbol_company = %s" % symbol_company)

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

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
    :type db: DbConnection
    :return:
    """
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    if not id_portfolio:
        id_portfolio = create_portfolio()

    print('Simulation start')


def get_info_simulation(id_simulation, db=None):
    """
    Get information of simulation as id of simulation
    :param id_simulation: id of simulation
    :type id_simulation: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: information on simulation
    :rtype: list[dict]
    """
    if not id_simulation:
        raise ValueError('ID simulation is None.')

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_portfolio, parameters, results
                FROM simulation WHERE id_simulation = %(id_simulation)s"""
    res = db.select_in_db(query, {'id_simulation': id_simulation})
    return_value = []
    for id_portfolio, parameters, results in res:
        return_value.append({'id_portfolio': id_portfolio, 'parameters': parameters, 'results': results})
    return return_value


def get_transaction_simulation(id_simulation, db=None):
    """
    Get transaction of simulation as id of simulation
    :param id_simulation: id of simulation
    :type id_simulation: int
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: transaction of simulation
    :rtype: list[dict]
    """
    if not id_simulation:
        raise ValueError('ID simulation is None.')

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT id_transaction, id_portfolio, id_symbol, quantity, value_current, transaction_date
                FROM "transaction" WHERE id_simulation = %(id_simulation)s"""
    res = db.select_in_db(query, {'id_simulation': id_simulation})
    return_value = []
    for id_transaction, id_portfolio, id_symbol, quantity, value_current, transaction_date in res:
        return_value.append({'id_transaction': id_transaction, 'id_portfolio': id_portfolio, 'id_symbol': id_symbol,
                             'quantity': quantity, 'value_current': value_current, 'transaction_date': transaction_date})
    return return_value

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(locals()[sys.argv[1]](sys.argv[2:]))
