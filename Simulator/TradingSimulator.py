import configparser
from DbConnection import DbConnection
from Broker import Broker
import Filters
from datetime import datetime


def main_simulator(initial_liquidity):
    # TODO: Pass parameters
    # TODO: Keep log?
    # Open a database connection for the queries
    config = configparser.ConfigParser()
    config.read('../config.ini')
    db = DbConnection(config.get('database', 'HOST'),
                      config.get('database', 'USER'),
                      config.get('database', 'PASSWORD'),
                      config.get('database', 'DATABASE'))
    log = open(config.get('path', 'path_log_simulator'), 'a')

    # TODO: ONLY FOR TESTING
    broker = Broker(initial_liquidity, db, log, min_value=500, max_value=2000)
    # broker.set_flat_fee_commission(5.25)
    broker.add_sell_filters()
    broker.add_buy_filters(Filters.FilterPriceGreaterThan(value=50),
                           Filters.FilterPriceLesserThan(value=100),
                           Filters.FilterPriceGreaterThan(value=75))
    broker.run_simulation()
    # TODO: ONLY FOR TESTING

if __name__ == "__main__":
    main_simulator(1000000)
