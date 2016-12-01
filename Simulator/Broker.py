from enum import Enum
import random
from Portfolio import Portfolio
from Market import Market
from datetime import datetime


#########################################################################################################
#                                           ENUM
#########################################################################################################

class _TypeCommission(Enum):
    """Enumeration of all possible types of commissions for a given transaction.

    percent: The commission is based on a percentage of the value of the transaction done.
    flat_fee: The commission is a fixed fee for every transaction done.
    none: There is no commission.
    """
    percent = 1
    flat_fee = 2
    none = 3


#########################################################################################################
#                                           Broker
#########################################################################################################
class Broker:
    # TODO: Keep log?
    def __init__(self, initial_liquidity, db, log,
                 min_date=datetime(2006, 1, 3), max_date=datetime(2016, 11, 4),
                 min_value=0, max_value=float("inf")):
        # TODO: Add comment
        # The Market where the broker is buying and selling stocks
        self._market = Market(min_date, max_date, db)

        # TODO: LOG
        self.log = log

        # The portfolio contains all the stocks bought for the current day and time and
        # the cash money that can be used instantly by the broker to buy stocks.
        self._portfolio = Portfolio(initial_liquidity, min_value, max_value, log)

        # The bill is how much the broker has charged for its services.
        # TODO : Make something of it
        self._bill = 0.0

        # Dictionary that keeps track of the value of our portfolio at any given time since the start of the simulation.
        # Key: Date ; Value: Total of our assets for any given
        self._hist_market_value = {}

        # A commission is how much the broker is asking to get paid for a given transaction.
        # Initially, there is no commission. It must be added with a setter.
        self._commission = self._Commission(_TypeCommission.none)

        # Filters are functions used to select which companies should be in our portfolio at any given time.
        self._sell_filters = []
        self._buy_filters = []

    #######################################################################################################
    #                                      Commission
    #######################################################################################################

    class _Commission:
        def __init__(self, type_commission, commission_val=None):
            """Represent a commission charged by the broker to execute a transaction.

            An instance of _Commission should always be created by one of the two functions
            set_flat_fee_commission() and set_percent_commission().

            :param type_commission: An instance of _TypeCommission. (Percent, Flat Fee or None)
            :type type_commission: _TypeCommission
            :param commission_val: The value of the commission. In % or $ depending of its type.
            :type commission_val: float | int
            :return: Nothing
            """
            self.value = commission_val
            self.type = type_commission

        def calculate(self, transaction_value):
            """Calculate the commission that the broker should charge to the client for the transaction.

            :param transaction_value: The value in $ of the transaction made (buy or sell)
            :type transaction_value: float | int
            :return: The commission that should be charged by the broker for this transaction.
            :rtype: float | int
            """
            if self.type == _TypeCommission.percent:
                return transaction_value * self.value
            elif self.type == _TypeCommission.flat_fee:
                return self.value
            else:
                return 0

    def set_flat_fee_commission(self, value):
        """Set the commission of the broker to a flat fee for any transaction done.

        :param value: The flat fee that will be charged for any transaction. Must be > 0.
        :type value: float | int
        :return: Nothing
        """
        if value > 0:
            self._commission = self._Commission(_TypeCommission.flat_fee, value)
        else:
            raise ValueError

    def set_percent_commission(self, value):
        """Set the commission of the broker to a percentage of any transaction done.

        :param value: Percentage of the transaction that will be charged. Must be > 0. 0.5 => 0.005%
        :type value: float | int
        :return: Nothing
        """
        if value > 0:
            self._commission = self._Commission(_TypeCommission.percent, value/100)
        else:
            raise ValueError

    #######################################################################################################
    #                                         Filters
    #######################################################################################################

    def add_sell_filters(self, *filters):
        """Add one or many filters to reduce the list of companies in our portfolio.

        Functions are regrouped in "Filters.py". They must take as parameters a list of strings, an
        object "Market" and an object "Portfolio".
        The list contains all symbols of the companies in our portfolio that will be sold.
        The "Market" is an instance of the class "Market"; ditto for "Portfolio".

        The filter function must return the same type of list as the one in the parameters. It should be
        reduced to remove all companies in our portfolio that we want to keep because they satisfy a
        specific criterion (or many criteria).

        :param filters: One or many functions as described above.
        :return: Nothing
        """
        for f in filters:
            self._sell_filters.append(f)

    def add_buy_filters(self, *filters):
        """Add one or many filters to reduce the list of companies where we should invest.

        Functions are regrouped in "Filters.py". They must take as parameters a list of strings, an
        object "Market" and an object "Portfolio".
        The list contains all symbols of the companies in our portfolio that will be sold.
        The "Market" is an instance of the class "Market"; ditto for "Portfolio".

        The function must return the same type of list as the one in the parameters. It should be reduced
        to remove all companies where we don't want to invest because they don't satisfy a specific
        criterion (or many criteria).

        :param filters: One or many functions as described above.
        :return: Nothing
        """
        for f in filters:
            self._buy_filters.append(f)

    #######################################################################################################
    #                                Run the simulation
    #######################################################################################################

    def _sell(self):
        # TODO : Comment
        # Get the list of all companies that we can sell (those we have in our portfolio);
        lst = self._portfolio.get_companies()

        # Filter the list to only keep the companies that should be sold;
        for f in self._sell_filters:
            lst = f.run(lst, self._market, self._portfolio)

        # For all companies that we should sell, sell 'em;
        for symbol in lst:
            # Instruct the portfolio to sell all stocks it has for this company
            gain = self._portfolio.sell_all_stocks(symbol, self._market.get_price(symbol))

            # If it succeeded, calculate the commission
            if gain > 0:
                commission = self._commission.calculate(gain)
                self._bill += commission

    def _buy(self):
        # TODO: Comment
        # Get the list of all companies that we can buy (those trading that day in the market);
        lst = self._market.get_trading_stocks()

        # Filter the list to only keep the companies that we should buy;
        # TODO : Remove those that we already have and which are maxed out.
        for f in self._buy_filters:
            lst = f.run(lst, self._market, self._portfolio)

        # For all companies that we should buy, as long as we have money, buy 'em (random order)
        random.shuffle(lst)
        for symbol in lst:
            # Attempt to buy as many stocks as possible for this company
            # TODO : Allow to choose a different algorithm for buying
            cost = self._portfolio.maximize_buy(symbol, self._market.get_price(symbol))

            # If it succeeded, calculate the commission
            if cost > 0:
                commission = self._commission.calculate(cost)
                self._bill += commission

            # Validate if we can continue to buy
            if not self._portfolio.can_buy():
                break

    def _tracking(self):
        # TODO : Add the draw(), data structure to keep track of value over time & maybe more
        self._hist_market_value[self._market.get_current_date()] = \
            self._portfolio.get_assets_value(self._market) - self._bill
        # TODO : Remove the print
        print("{}: {}\tBill:{}".format(self._market.get_current_date(),
                                       self._hist_market_value[self._market.get_current_date()],
                                       self._bill))

    def run_simulation(self):
        # TODO: Comment
        # As long as there is a new business day in our simulation;
        trading = True
        while trading:
            # TODO : Log
            self.log.write("{}\n".format(self._market.get_current_date()))

            # Sell companies in our portfolio that satisfy our criteria for selling;
            self._sell()

            # If we have enough money, buy companies trading this day that satisfy our criteria for buying;
            if self._portfolio.can_buy():
                self._buy()

            # Keep track of our assets
            self._tracking()

            # Go to the next trading day.
            trading = self._market.next()
        # TODO: Remove the print, instead, print a résumé in the log.
        self._portfolio.print_portfolio()