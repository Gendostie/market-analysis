import configparser
from DbConnection import DbConnection
from Broker import Broker
import Filters


def main_simulator(initial_liquidity):
    # TODO: Pass parameters
    # Open a database connection for the queries
    config = configparser.ConfigParser()
    config.read('../config.ini')
    db = DbConnection(config.get('database', 'HOST'),
                      config.get('database', 'USER'),
                      config.get('database', 'PASSWORD'),
                      config.get('database', 'DATABASE'))
    log_broker = config.get('path', 'path_log_broker')
    log_port = config.get('path', 'path_log_portfolio')

    # TODO: ONLY FOR TESTING
    broker = Broker(db, initial_liquidity, log_broker, log_port, min_value=0, max_value=2000)
    # broker.set_percent_commission(1)
    broker.add_max_nb_of_stocks_to_buy(1)
    # broker.add_sell_filters(Filters.FilterNot())
    # broker.add_buy_filters(Filters.FilterNotInPortfolio())
    broker.add_sell_filters(Filters.FilterVIP(), Filters.FilterHistorical())
    broker.add_buy_filters()
    broker.run_simulation()
    # TODO: ONLY FOR TESTING

if __name__ == "__main__":
    main_simulator(1000000)
