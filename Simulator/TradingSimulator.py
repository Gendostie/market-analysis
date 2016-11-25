import configparser
from DbConnection import DbConnection
from Broker import Broker
import Filters
from datetime import datetime


def main_simulator(initial_liquidity):
    # TODO: Pass parameters
    # Open a database connection for the queries
    config = configparser.ConfigParser()
    config.read('../config.ini')
    db = DbConnection(config.get('database', 'HOST'),
                      config.get('database', 'USER'),
                      config.get('database', 'PASSWORD'),
                      config.get('database', 'DATABASE'))

    # TODO: ONLY FOR TESTING
    broker = Broker(initial_liquidity, db, min_date=datetime(2016, 10, 1), max_value=1000)
    broker.set_percent_commission(2)
    broker.add_sell_filters(Filters.fl_not)
    broker.run_simulation()
    # TODO: ONLY FOR TESTING

if __name__ == "__main__":
    main_simulator(1000000)
