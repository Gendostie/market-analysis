import finsymbols
import math
from datetime import timedelta
from QT.Singleton import divide

try:
    from DbConnection import DbConnection
except ImportError:
    from Manager_DB.DbConnection import DbConnection


# TODO : Config
HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'market_analysis'


def get_snp500(db=None):
    """
    Get company with flag is_in_snp500 in db
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: result in list of dict,
        ex: [{'symbol': 'GOOGL', 'last_update_historic': None, 'name': 'Alphabet Inc Class A', 'is_in_snp500': '\\x01'}]
    :rtype: list[dict]
    """
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
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
    :type db: DbConnection
    :return: number row affected
    :rtype: int
    """
    if not symbol or not name:
        raise ValueError('Name or symbol is None. name: %(name)s ; symbol: %(symbol)s ' % locals())

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    # Add new company not in table and update name and flag snp500 if already in table
    query = """INSERT INTO company (name, symbol, is_in_snp500)
               VALUES (%(name)s, UPPER(%(symbol)s), 1)
               ON DUPLICATE KEY UPDATE name = %(name)s, is_in_snp500 = 1"""
    return db.modified_db(query, {'name': name, 'symbol': symbol})


def get_company_by_symbol(symbol, db=None):
    """
    Get information in table company  as symbol of company
    :param symbol: symbol of a company we search
    :type symbol: str
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: return list of dict of company who correspond to symbol
    :rtype: list[dict]
    """
    if not symbol:
        raise ValueError('Symbol company is None.')

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
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
    :type db: DbConnection
    :return: return list of dict of company who correspond to name
    :rtype: list[dict]
    """
    if not name:
        raise ValueError('Name company is None.')

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT name, symbol, is_in_snp500, last_update_historic
                FROM company WHERE name = %(name)s"""
    res = db.select_in_db(query, {'name': name})
    return_value = []
    for name, symbol, is_in_snp500, last_update_historic in res:
        return_value.append({'name': name, 'symbol': symbol, 'is_in_snp500': is_in_snp500,
                             'last_update_historic': last_update_historic})
    return return_value


def get_historic_value_all_company(db=None):
    """
    Get historic value of all company
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: return list of dict
    :rtype: list[dict]
    """
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT c.name, c.symbol, d.date_daily_value, d.adj_close, date_historic_value, revenu_usd_mil,
                gross_margin_pct, net_income_usd_mil, earning_per_share_usd, dividends_usd, book_value_per_share_usd,
                free_cash_flow_per_share_usd
                FROM company c LEFT JOIN historic_value hv ON c.symbol = hv.id_symbol
                               LEFT JOIN daily_value d ON c.symbol = d.id_symbol
                WHERE c.is_in_snp500 AND hv.date_historic_value = (SELECT max(date_historic_value)
                                                                   FROM historic_value
                                                                   WHERE id_symbol = c.symbol)
                                     AND d.date_daily_value = (SELECT max(date_daily_value)
                                                               FROM daily_value
                                                               WHERE id_symbol = c.symbol);"""
    res = db.select_in_db(query)
    return_value = []
    for company_name, symbol, date_daily_value, adj_close, \
        datetime_value, revenue, gross_margin, income, earning, dividends, book_value, cash_flow in res:
        # TODO: Add comment
        result_52wk = ()
        addedDays = 0
        while len(result_52wk) == 0:
            new_date = date_daily_value.replace(year=date_daily_value.year - 1) + timedelta(days=addedDays)

            query_2 = """SELECT adj_close
                         FROM daily_value
                         WHERE date_daily_value = "{}"
                               AND id_symbol = "{}";""".format(new_date, symbol)
            result_52wk = db.select_in_db(query_2)
            addedDays += 1
        last_year_close = result_52wk[0][0]

        # If dividends = None, we change it to 0
        if dividends is None:
            dividends = 0

        return_value.append({'company_name': company_name,
                             'symbol': symbol,
                             'datetime_value': datetime_value,
                             'Revenue (Mil)': revenue,
                             'Gross Margin (%)': gross_margin,
                             'Net Income (Mil)': income,
                             'EPS': earning,
                             'Dividends': dividends,
                             'BVPS': book_value,
                             'FCFPS': cash_flow,
                             'datetime_daily_value': date_daily_value,
                             'Adj. Close': adj_close,
                             'Div. Yield (%)': divide(dividends, adj_close, 100),
                             'P/E Ratio': divide(adj_close, earning),
                             'P/B Ratio': divide(adj_close, book_value),
                             '52wk (%)': divide(adj_close - last_year_close, last_year_close, 100)})
    return return_value


# TODO: test to show plot qt
def get_daily_values(db=None):
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT date_daily_value, adj_close FROM daily_value WHERE id_symbol = 'GOOGL' ORDER BY date_daily_value"""
    res = db.select_in_db(query)
    return_value = []
    for date, value in res:
        return_value.append({'date': date, 'value': value})
    return return_value


#######################################################################################################################
#
#                                                GET MIN/MAX
#
#
#######################################################################################################################

# TODO : Error management when nothing in the database
def get_minimum_value_daily(value, db=None):
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT MIN({})
             FROM company c LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
             WHERE is_in_snp500 AND dv.date_daily_value = (SELECT MAX(dv1.date_daily_value)
                                                              FROM daily_value dv1
                                                              WHERE dv1.id_symbol = c.symbol);""".format(value)
    return math.floor(db.select_in_db(query)[0][0])


def get_maximum_value_daily(value, db=None):
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT MAX({})
             FROM company c LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
             WHERE is_in_snp500 AND dv.date_daily_value = (SELECT MAX(dv1.date_daily_value)
                                                              FROM daily_value dv1
                                                              WHERE dv1.id_symbol = c.symbol);""".format(value)
    return math.ceil(db.select_in_db(query)[0][0])


# TODO : Add comments
def get_minimum_value_historical(value, db=None):
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT MIN({})
             FROM company c LEFT JOIN historic_value hv ON c.symbol = hv.id_symbol
             WHERE is_in_snp500 AND hv.date_historic_value = (SELECT MAX(hv1.date_historic_value)
                                                              FROM historic_value hv1
                                                              WHERE hv1.id_symbol = c.symbol);""".format(value)
    return math.floor(db.select_in_db(query)[0][0])


def get_maximum_value_historical(value, db=None):
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    query = """SELECT MAX({})
             FROM company c LEFT JOIN historic_value hv ON c.symbol = hv.id_symbol
             WHERE is_in_snp500 AND hv.date_historic_value = (SELECT MAX(hv1.date_historic_value)
                                                              FROM historic_value hv1
                                                              WHERE hv1.id_symbol = c.symbol);""".format(value)
    return math.ceil(db.select_in_db(query)[0][0])


def get_minimum_value_calculation(name_calculation, db=None):
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    if name_calculation == "dividend_yield":
        query = """SELECT MIN(hv.dividends_usd / dv.adj_close) * 100
                   FROM company c LEFT JOIN historic_value hv ON c.symbol = hv.id_symbol
                                  LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
                    WHERE c.is_in_snp500 AND hv.date_historic_value = (SELECT MAX(hv1.date_historic_value)
                                                                       FROM historic_value hv1
                                                                       WHERE hv1.id_symbol = c.symbol)
                                         AND dv.date_daily_value = (SELECT MAX(dv1.date_daily_value)
                                                                    FROM daily_value dv1
                                                                    WHERE dv1.id_symbol = c.symbol);"""
        return math.floor(db.select_in_db(query)[0][0])
    elif name_calculation == "p_e_ratio":
        query = """SELECT MIN(dv.adj_close / hv.earning_per_share_usd)
                   FROM company c LEFT JOIN historic_value hv ON c.symbol = hv.id_symbol
                                  LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
                    WHERE c.is_in_snp500 AND hv.date_historic_value = (SELECT MAX(hv1.date_historic_value)
                                                                       FROM historic_value hv1
                                                                       WHERE hv1.id_symbol = c.symbol)
                                         AND dv.date_daily_value = (SELECT MAX(dv1.date_daily_value)
                                                                    FROM daily_value dv1
                                                                    WHERE dv1.id_symbol = c.symbol);"""
        return math.floor(db.select_in_db(query)[0][0])
    elif name_calculation == "p_b_ratio":
        query = """SELECT MIN(dv.adj_close / hv.book_value_per_share_usd)
                   FROM company c LEFT JOIN historic_value hv ON c.symbol = hv.id_symbol
                                  LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
                    WHERE c.is_in_snp500 AND hv.date_historic_value = (SELECT MAX(hv1.date_historic_value)
                                                                       FROM historic_value hv1
                                                                       WHERE hv1.id_symbol = c.symbol)
                                         AND dv.date_daily_value = (SELECT MAX(dv1.date_daily_value)
                                                                    FROM daily_value dv1
                                                                    WHERE dv1.id_symbol = c.symbol);"""
        return math.floor(db.select_in_db(query)[0][0])
    elif name_calculation == "52wk":
        min_val = float("inf")
        query_now = """SELECT adj_close, date_daily_value, c.symbol
                       FROM company c LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
                       WHERE date_daily_value = (SELECT MAX(dv1.date_daily_value)
                                                 FROM daily_value dv1
                                                 WHERE dv1.id_symbol = c.symbol);"""
        result_now = db.select_in_db(query_now)
        for close, date, symbol in result_now:
            # TODO: Add comment
            result_52wk = ()
            added_days = 0
            while len(result_52wk) == 0:
                new_date = date.replace(year=date.year - 1) + timedelta(days=added_days)

                query_2 = """SELECT adj_close
                             FROM daily_value
                             WHERE date_daily_value = "{}"
                                   AND id_symbol = "{}";""".format(new_date, symbol)
                result_52wk = db.select_in_db(query_2)
                added_days += 1
            last_year_close = result_52wk[0][0]

            tmp_min = divide(close - last_year_close, last_year_close, 100)
            if float(tmp_min) < min_val:
                min_val = float(tmp_min)

        return math.floor(min_val)
    else:
        return 0


def get_maximum_value_calculation(name_calculation, db=None):
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
    if name_calculation == "dividend_yield":
        query = """SELECT MAX(hv.dividends_usd / dv.adj_close) * 100
                   FROM company c LEFT JOIN historic_value hv ON c.symbol = hv.id_symbol
                                  LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
                    WHERE c.is_in_snp500 AND hv.date_historic_value = (SELECT MAX(hv1.date_historic_value)
                                                                       FROM historic_value hv1
                                                                       WHERE hv1.id_symbol = c.symbol)
                                         AND dv.date_daily_value = (SELECT MAX(dv1.date_daily_value)
                                                                    FROM daily_value dv1
                                                                    WHERE dv1.id_symbol = c.symbol);"""
        return math.ceil(db.select_in_db(query)[0][0])
    elif name_calculation == "p_e_ratio":
        query = """SELECT MAX(dv.adj_close / hv.earning_per_share_usd)
                   FROM company c LEFT JOIN historic_value hv ON c.symbol = hv.id_symbol
                                  LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
                    WHERE c.is_in_snp500 AND hv.date_historic_value = (SELECT max(hv1.date_historic_value)
                                                                       FROM historic_value hv1
                                                                       WHERE hv1.id_symbol = c.symbol)
                                         AND dv.date_daily_value = (SELECT max(dv1.date_daily_value)
                                                                    FROM daily_value dv1
                                                                    WHERE dv1.id_symbol = c.symbol);"""
        return math.ceil(db.select_in_db(query)[0][0])
    elif name_calculation == "p_b_ratio":
        query = """SELECT MAX(dv.adj_close / hv.book_value_per_share_usd)
                   FROM company c LEFT JOIN historic_value hv ON c.symbol = hv.id_symbol
                                  LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
                    WHERE c.is_in_snp500 AND hv.date_historic_value = (SELECT max(hv1.date_historic_value)
                                                                       FROM historic_value hv1
                                                                       WHERE hv1.id_symbol = c.symbol)
                                         AND dv.date_daily_value = (SELECT max(dv1.date_daily_value)
                                                                    FROM daily_value dv1
                                                                    WHERE dv1.id_symbol = c.symbol);"""
        return math.ceil(db.select_in_db(query)[0][0])
    elif name_calculation == "52wk":
        max_val = float("-inf")
        query_now = """SELECT adj_close, date_daily_value, c.symbol
                       FROM company c LEFT JOIN daily_value dv ON c.symbol = dv.id_symbol
                       WHERE date_daily_value = (SELECT MAX(dv1.date_daily_value)
                                                 FROM daily_value dv1
                                                 WHERE dv1.id_symbol = c.symbol);"""
        result_now = db.select_in_db(query_now)
        for close, date, symbol in result_now:
            # TODO: Add comment
            result_52wk = ()
            addedDays = 0
            while len(result_52wk) == 0:
                new_date = date.replace(year=date.year - 1) + timedelta(days=addedDays)

                query_2 = """SELECT adj_close
                             FROM daily_value
                             WHERE date_daily_value = "{}"
                                   AND id_symbol = "{}";""".format(new_date, symbol)
                result_52wk = db.select_in_db(query_2)
                addedDays += 1
            last_year_close = result_52wk[0][0]

            tmp_max = divide(close - last_year_close, last_year_close, 100)
            if float(tmp_max) > max_val:
                max_val = float(tmp_max)

        return math.ceil(max_val)
    else:
        return 0


def get_minimum_maximum_value_date_daily(db=None):
    """
    Get datetime min and max in table historical of db
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: Datetime min and max in table historical of db
    :rtype: tuple(datetime.datetime)
    """
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """SELECT MIN(date_daily_value), MAX(date_daily_value) FROM daily_value"""
    return db.select_in_db(query)[0]


#######################################################################################################################
#                                                                                                                     #
#                                                                                                                     #
#######################################################################################################################


def update_snp550_to_db(db=None):
    """
    Update data of table company to check if we have new company and remove company not in new list s&p500
    :param db: if we have already connexion in other function who cal this function
    :type db: DbConnection
    :return: number row affected
    :rtype: int
    """
    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)
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
    :type db: DbConnection
    :return: number row affected
    :rtype: int
    """
    if not symbol_company:
        raise ValueError('Symbol company is None.')
    if len(list_values) < 1:
        raise ValueError('List of values is empty. %s' % list_values)

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """INSERT INTO daily_value (date_daily_value, id_symbol, close_val, adj_close)
               VALUES (%(datetime_value)s, %(symbol_company)s, %(close_value)s, %(adj_close_value)s)
               ON DUPLICATE KEY UPDATE date_daily_value = %(datetime_value)s,
                                       close_val = %(close_value)s,
                                       adj_close = %(adj_close_value)s"""

    params = {'datetime_value': list_values[0],
              'symbol_company': symbol_company,
              'close_value': list_values[1],
              'adj_close_value': list_values[2]}
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
    :type db: DbConnection
    :return: number row affected
    :rtype: int
    """
    if not symbol_company:
        raise ValueError('Symbol company is None.')
    if len(list_values) < 1:
        raise ValueError('List of values is empty. %s' % list_values)

    if not db or type(db) is not DbConnection:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

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

    params = {'datetime_value': list_values[0], 'symbol_company': symbol_company, 'revenue': list_values[1],
              'gross_margin': list_values[2], 'income': list_values[3], 'earning': list_values[4],
              'dividends': list_values[5],
              'book_value': list_values[6], 'cash_flow': list_values[7]}
    # TODO: check for multi-row to insert, maybe use connection.executemany(query, list of tuple values)
    db.modified_db(query, params)

    return 0


def insert_dividend_to_db(symbol_company, datetime, dividend, db=None):
    """Insert one line in the table "dividends". Represent a dividend paid by a company at a specific date.

    :param symbol_company: The symbol of the company.
    :param datetime: A Datetime object which represents the date when the dividend was paid by the company.
    :param dividend: A float. The actual dividend paid by the company on that date.
    :param db: A DbConnection object. If nothing is passed, a new connection will be made with the default db params.
    :return: Nothing. The insertion will be made in the table "dividends"
    """
    if not symbol_company:
        raise ValueError('symbol_company is None.')

    if not db:
        db = DbConnection(HOST, USER, PASSWORD, DATABASE)

    query = """INSERT INTO dividends (symbol, date_dividend, dividend)
               VALUES (%(symbol_value)s, %(datetime_value)s, %(dividend_value)s)
               ON DUPLICATE KEY UPDATE date_dividend = %(datetime_value)s,
                                       dividend = %(dividend_value)s"""
    params = {'symbol_value': symbol_company,
              'datetime_value': datetime,
              'dividend_value': dividend}
    db.modified_db(query, params)

    return 0
