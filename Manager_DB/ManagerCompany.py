#!/usr/bin/python
import finsymbols
import sys
from DbConnection import DBConnection

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'market_analysis'


def get_snp500(db=None):
    """
    Get company with flag is_in_snp500 in db
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: result in list of dict,
        ex: [{'symbol': 'GOOGL', 'last_update_historic': None, 'name': 'Alphabet Inc Class A', 'is_in_snp500': '\\x01'}]
    :rtype: list[dict]
    """
    if not db or type(db) is not DBConnection:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT name, symbol, last_update_historic
                FROM company WHERE is_in_snp500 = 1"""
    res = db.select_in_db(query)
    return_value = []
    for name, symbol, last_update_historic in res:
        return_value.append({'name': name, 'symbol': symbol, 'last_update_historic': last_update_historic})
    return return_value


def add_company_to_db(symbol, name, db=None):
    """
    Add a company to table company
    :param symbol: symbol of company in stock market
    :type symbol: str
    :param name: name of company in stock market
    :type name: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: number row affected
    :rtype: int
    """
    if not symbol or not name:
        raise ValueError('Name or symbol is None. name: %(name)s ; symbol: %(symbol)s ' % locals())

    if not db or type(db) is not DBConnection:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    # Add new company not in table and update name and flag snp500 if already in table
    query = """INSERT INTO company (name, symbol, is_in_snp500) VALUES (%(name)s, UPPER(%(symbol)s), 1)
                ON DUPLICATE KEY UPDATE name = %(name)s, is_in_snp500 = 1"""
    return db.modified_db(query, {'name': name, 'symbol': symbol})


def get_company_by_symbol(symbol, db=None):
    """
    Get information in table company  as symbol of company
    :param symbol: symbol of a company we search
    :type symbol: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: return list of dict of company who correspond to symbol
    :rtype: list[dict]
    """
    if not symbol:
        raise ValueError('Symbol company is None.')

    if not db or type(db) is not DBConnection:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT name, symbol, is_in_snp500, last_update_historic
                FROM company WHERE symbol = %(symbol)s"""
    res = db.select_in_db(query, {'symbol': symbol})
    return_value = []
    for name, symbol, is_in_snp500, last_update_historic in res:
        return_value.append({'name': name, 'symbol': symbol, 'is_in_snp500': is_in_snp500,
                             'last_update_historic': last_update_historic})
    return return_value


def get_company_by_name(name, db=None):
    """
    Get information in table company  as name of company
    :param name: name of a company we search
    :type name: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: return list of dict of company who correspond to name
    :rtype: list[dict]
    """
    if not name:
        raise ValueError('Name company is None.')

    if not db or type(db) is not DBConnection:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT name, symbol, is_in_snp500, last_update_historic
                FROM company WHERE name = %(name)s"""
    res = db.select_in_db(query, {'name': name})
    return_value = []
    for name, symbol, is_in_snp500, last_update_historic in res:
        return_value.append({'name': name, 'symbol': symbol, 'is_in_snp500': is_in_snp500,
                             'last_update_historic': last_update_historic})
    return return_value


def get_historic_value_company(symbol, db=None):
    """
    Get historic value of a company
    :param symbol: symbol of a company we search
    :type symbol: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: return list of dict of historic value a company who correspond to symbol
    :rtype: list[dict]
    """
    if not symbol:
        raise ValueError('Symbol company is None.')

    if not db or type(db) is not DBConnection:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT c.name, c.symbol, date_historic_value, revenu_usd_mil, gross_margin_pct,
                net_income_usd_mil, earning_per_share_usd, dividends_usd, book_value_per_share_usd,
                free_cash_flow_per_share_usd
                FROM company c left join historic_value hv on c.symbol = hv.id_symbol
                WHERE c.symbol = %(symbol)s"""
    res = db.select_in_db(query, {'symbol': symbol})
    return_value = []
    for company_name, symbol, datetime_value, revenue, gross_margin, income, earning, dividends, book_value, cash_flow in res:
        return_value.append({'company_name': company_name, 'symbol': symbol, 'datetime_value': datetime_value, 'revenue': revenue,
                             'gross_margin': gross_margin, 'income': income, 'earning': earning, 'dividends': dividends,
                             'book_value': book_value, 'cash_flow': cash_flow})
    return return_value


def get_historic_value_all_company(db=None):
    """
    Get historic value of all company
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: return list of dict
    :rtype: list[dict]
    """
    if not db or type(db) is not DBConnection:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT c.name, c.symbol, date_historic_value, revenu_usd_mil, gross_margin_pct,
                net_income_usd_mil, earning_per_share_usd, dividends_usd, book_value_per_share_usd,
                free_cash_flow_per_share_usd
                FROM company c left join historic_value hv on c.symbol = hv.id_symbol"""
    res = db.select_in_db(query)
    return_value = []
    for company_name, symbol, datetime_value, revenue, gross_margin, income, earning, dividends, book_value, cash_flow in res:
        return_value.append({'company_name': company_name, 'symbol': symbol, 'datetime_value': datetime_value, 'revenue': revenue,
                             'gross_margin': gross_margin, 'income': income, 'earning': earning, 'dividends': dividends,
                             'book_value': book_value, 'cash_flow': cash_flow})
    return return_value


def update_snp550_to_db(db=None):
    """
    Update data of table company to check if we have new company and remove company not in new list s&p500
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: number row affected
    :rtype: int
    """
    if not db or type(db) is not DBConnection:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    # Set all company in table for to re-init to 0 flag is_in_snp500
    query = """UPDATE company SET is_in_snp500 = 0"""
    db.modified_db(query)

    snp500 = finsymbols.get_sp500_symbols()
    # update and add_company of s500
    for company in snp500:
        add_company_to_db(company.get('symbol'), company.get('company'), db)

    # TODO: call fct to historic data in csv [Gen]
    return 0


def insert_daily_value_to_db(symbol_company, list_values, db=None):
    """
    Values to insert in table daily_value of db for a company
    :param symbol_company: symbol of a company
    :type symbol_company: str
    :param list_values: list of list of values
    :type list_values: list[list[str, str, str]]
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: number row affected
    :rtype: int
    """
    if not symbol_company:
        raise ValueError('Symbol company is None.')
    if len(list_values) < 1:
        raise ValueError('List of values is empty. %s' % list_values)

    if not db or type(db) is not DBConnection:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    query = """INSERT INTO daily_value (date_daily_value, id_symbol, stock_value, 52w_price_change)
                VALUES (%(datetime_value)s, %(symbol_company)s, %(stock_value)s, %(price_change)s)
                ON DUPLICATE KEY UPDATE date_daily_value = %(datetime_value)s, stock_value = %(stock_value)s,
                                        52w_price_change = %(price_change)s"""
    for datetime_value, stock_value, price_change in list_values:
        # check if datetime_value None, if None we continue with next row
        if not datetime_value:
            print("Value of date_daily_value is None for company %s. params = " % symbol_company,
                  (datetime_value, stock_value, price_change))
            continue
        params = {'datetime_value': datetime_value, 'symbol_company': symbol_company, 'stock_value': stock_value,
                  'price_change': price_change}
        # TODO: check for multi-row to insert, maybe use connection.executemayny(query, list of tuple values)
        db.modified_db(query, params)

    return 0


def insert_historic_value_to_db(symbol_company, list_values, db=None):
    """
    Values to insert in table historic_value of db for a company
    :param symbol_company: symbol of a company
    :type symbol_company: str
    :param list_values: list of list of values
    :type list_values: list[list[str, str, str, str, str, str, str, str, str]]
    :param db: if we have already connexion in other function who cal this function
    :type db: DBConnection
    :return: number row affected
    :rtype: int
    """
    if not symbol_company:
        raise ValueError('Symbol company is None.')
    if len(list_values) < 1:
        raise ValueError('List of values is empty. %s' % list_values)

    if not db or type(db) is not DBConnection:
        db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    query = """INSERT INTO historic_value (date_historic_value, id_symbol, revenu_usd_mil,
                                                           gross_margin_pct, net_income_usd_mil, earning_per_share_usd,
                                                           dividends_usd, book_value_per_share_usd,
                                                           free_cash_flow_per_share_usd)
               VALUES (%(datetime_value)s, %(symbol_company)s, %(revenue)s, %(gross_margin)s, %(income)s,
                       %(earning)s, %(dividends)s, %(book_value)s, %(cash_flow)s)
               ON DUPLICATE KEY UPDATE revenu_usd_mil = %(revenue)s, gross_margin_pct = %(gross_margin)s,
                                       net_income_usd_mil = %(income)s, earning_per_share_usd = %(earning)s,
                                       dividends_usd = %(dividends)s, book_value_per_share_usd = %(book_value)s,
                                       free_cash_flow_per_share_usd = %(cash_flow)s"""
    for datetime_value, revenue, gross_margin, income, earning, dividends, book_value, cash_flow in list_values:
        # check if datetime_value None, if None we continue with next row
        if not datetime_value:
            print("Value of date_daily_value is None for company %s. params = " % symbol_company,
                  (datetime_value, revenue, gross_margin, income, earning, dividends, book_value, cash_flow))
            continue
        params = {'datetime_value': datetime_value, 'symbol_company': symbol_company, 'revenue': revenue,
                  'gross_margin': gross_margin, 'income': income, 'earning': earning, 'dividends': dividends,
                  'book_value': book_value, 'cash_flow': cash_flow}
        # TODO: check for multi-row to insert, maybe use connection.executemayny(query, list of tuple values)
        db.modified_db(query, params)

    return 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(locals()[sys.argv[1]](sys.argv[2:]))
