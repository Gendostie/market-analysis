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
    log_broker = open(config.get('path', 'path_log_broker'), 'w')
    log_broker.write("date;cash;stocks_value;bill\n")
    log_port = open(config.get('path', 'path_log_portfolio'), 'w')
    log_port.write("date;type_transaction;symbol;nb_stocks;transaction_value\n")

    # TODO: ONLY FOR TESTING
    broker = Broker(initial_liquidity, db, log_broker, log_port, min_value=0, max_value=2000)
    # broker.set_percent_commission(1)
    broker.add_max_nb_of_stocks_to_buy(1)
    broker.add_sell_filters(Filters.FilterNot())
    broker.add_buy_filters(Filters.FilterNotInPortfolio())
    broker.run_simulation()
    # TODO: ONLY FOR TESTING

if __name__ == "__main__":
    main_simulator(100000)
