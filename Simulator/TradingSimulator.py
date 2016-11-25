import configparser
from DbConnection import DbConnection
from Market import Market
from Broker import Broker
import Filters
from datetime import datetime


def main_simulator(initial_liquidity, begin=None, end=None):
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

        # TODO: ONLY FOR TESTING
        broker = Broker(initial_liquidity, Market(begin, end, db), max_value=1000)
        broker.set_percent_commission(2)
        broker.add_sell_filters(Filters.fl_not)
        broker.run_simulation()
        # TODO: ONLY FOR TESTING


# TODO: ONLY FOR TESTING
def get_max_trading_date(db):
    query = """SELECT MAX(date_daily_value) FROM daily_value;"""
    return db.select_in_db(query)[0][0]


def get_min_trading_date(db):
    query = """SELECT MIN(date_daily_value) FROM daily_value;"""
    return db.select_in_db(query)[0][0]
# TODO: ONLY FOR TESTING

if __name__ == "__main__":
    main_simulator(1000000, begin=datetime(2016, 1, 1))
