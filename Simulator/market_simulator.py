import configparser
from datetime import datetime
from DbConnection import DbConnection
from Simulator.market import Market


def main_simulator(initial_value, transaction_cost, begin=None, end=None):
        # Open a database connection for the queries
        config = configparser.ConfigParser()
        config.read('../config.ini')
        db = DbConnection(config.get('database', 'HOST'),
                          config.get('database', 'USER'),
                          config.get('database', 'PASSWORD'),
                          config.get('database', 'DATABASE'))

        # Create the object Market
        if begin is None:
            begin = get_min_trading_date(db)
        if end is None:
            end = get_max_trading_date(db)
        market = Market(transaction_cost, begin, end, db)

        # TODO: ONLY FOR TESTING
        market.debug_print()
        cpt = 0
        flag = market.next()
        while flag:
            cpt +=1
            if cpt == 100:
                cpt == 0
                print(market.get_current_date())
            flag = market.next()
        market.debug_print()
        # TODO: ONLY FOR TESTING


def get_max_trading_date(db):
    query = """SELECT MAX(date_daily_value) FROM daily_value;"""
    date = db.select_in_db(query)[0][0]
    return datetime(date.year, date.month, date.day)


def get_min_trading_date(db):
    query = """SELECT MIN(date_daily_value) FROM daily_value;"""
    date = db.select_in_db(query)[0][0]
    return datetime(date.year, date.month, date.day)