from enum import Enum
import random
from Portfolio import Portfolio

#########################################################################################################
#                                           Commission
#########################################################################################################


class _TypeCommission(Enum):
    """Enumeration of all possible types of commissions.

    percent: The commission is based on a percentage of the value of the transaction done.
    flat_fee: The commission is a fixed fee for every transaction done.
    none: There is no commission.
    """
    percent = 1
    flat_fee = 2
    none = 3


class _Commission:
    def __init__(self, type_commission, commission_val=None):
        """Represent a commission for a type of transaction (sell or buy).

        The broker keeps an object of this class for when it buys and another one for when it sells.

        An instance of _Commission should always be created by one of the two functions
        flat_fee_commission() and percent_commission().

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


#########################################################################################################
#                                           TEST
#########################################################################################################

def perform(lst, market, filters):
    for f in filters:
        lst = f(lst, market)
    return lst


#########################################################################################################
#                                           Broker
#########################################################################################################
class Broker:
    def __init__(self, initial_liquidity, market):
        # The Market where the broker is buying and selling stocks
        self._market = market

        # The portfolio contains all the stocks bought for the current day and time and
        # the liquidity (cash money that can be used instantly by the broker to buy stocks).
        self._portfolio = Portfolio(initial_liquidity)

        # The bill is how much the broker has charged for its services.
        self._bill = 0.0

        # A commission is how much the broker is asking to get paid for a given transaction.
        # Initially, there is no commission.
        self._commission = _Commission(_TypeCommission.none)

        # Filters are functions used to select which companies should be in our portfolio at any given time.
        self._sell_filters = []
        self._buy_filters = []

    #######################################################################################################
    #                                Setters for the commission
    #######################################################################################################

    def set_flat_fee_commission(self, value):
        """Set the commission of the broker to a flat fee for any transaction done.

        :param value: The flat fee which is charged for any transaction. Must be > 0.
        :type value: float | int
        :return: Nothing
        """
        if value > 0:
            self._commission = _Commission(_TypeCommission.flat_fee, value)
        else:
            raise ValueError

    def set_percent_commission(self, value):
        """Set the commission of the broker to a percentage of any transaction done.

        :param value: The percent of the transaction value which is charged. Must be > 0 or between ]0,1].
        :type value: float | int
        :return: Nothing
        """
        if 0 < value <= 1:
            self._commission = _Commission(_TypeCommission.percent, value)
        elif value > 0:
            self._commission = _Commission(_TypeCommission.percent, value/100)
        else:
            raise ValueError

    #######################################################################################################
    #                                Setters for the filters
    #######################################################################################################

    def add_sell_filters(self, *filters):
        """Add one or many filters to reduce the list of companies in our portfolio.

        Functions are regrouped in "Filters.py". They must take as parameters a list of strings and an
        object "Market". The list contains all symbols of the companies in our portfolio that will be sold.
        The "Market" is an instance of the class "Market".

        The function must return the same type of list as the one in the parameters. It should be reduced
        to remove all companies in our portfolio that we want to keep because they satisfy a specific
        criterion (or many criteria).

        :param filters: One or many functions that take as parameters a list of strings and an object "Market"
        :return: Nothing
        """
        for f in filters:
            self._sell_filters.append(f)

    def add_buy_filters(self, *filters):
        """Add one or many filters to reduce the list of companies where we should invest.

        Functions are regrouped in "Filters.py". They must take as parameters a list of strings and an
        object "Market". The list contains all symbols of the companies where we can invest for that day.
        The "Market" is an instance of the class "Market".

        The function must return the same type of list as the one in the parameters. It should be reduced
        to remove all companies where we don't want to invest because they don't satisfy a specific
        criterion (or many criteria).

        :param filters: One or many functions that take as parameters a list of strings and an object "Market"
        :return: Nothing
        """
        for f in filters:
            self._buy_filters.append(f)

    def _how_many_stocks_to_buy(self, symbol):
        # TODO: Make a real function to calculate the number of stocks to buy.
        return 1

    #######################################################################################################
    #                                Run the simulation
    #######################################################################################################

    def _sell(self):
        # Get the list of all companies that we can sell (which is what we have in our portfolio);
        lst = self._portfolio.get_companies()

        # Filter the list to only keep the companies that should be sold;
        # TODO : Take into consideration the commission? Gain - commission > 0 ?
        for f in self._sell_filters:
            lst = f(lst, self._market, self._portfolio)

        # For all companies that we should sell, sell 'em;
        for symbol in lst:
            # Get how much you get for selling all the stocks in the market;
            gain = self._market.sell(symbol, self._portfolio.get_stocks_count(symbol))

            # Remove the stocks in our portfolio;
            # TODO: If gain == 0, what to do?
            self._portfolio.sell_all_stocks(symbol)

            # Calculate the commission;
            commission = self._commission.calculate(gain)
            self._bill += commission

            # Adjust the liquidity available.
            self._liquidity += (gain - commission)

    def _buy(self):
        # Get the list of all companies that we can buy;
        lst = self._market.get_trading_stocks()

        # Filter the list to only keep the companies that we should buy;
        # TODO : Remove those that we already have and which are maxed out.
        for f in self._buy_filters:
            lst = f(lst, self._market, self._portfolio)

        # For all companies that we should buy, as long as we have money, buy 'em (random order)
        # TODO : Minimum liquidity in portfolio?
        random.shuffle(lst)
        for symbol in lst:
            # Get the number of stocks that we should and can buy for this company
            nb_of_stocks = self._how_many_stocks_to_buy(symbol)

            # If it's greater than 0 stock, get how much you must pay to acquire them in the market
            if nb_of_stocks > 0:
                cost = self._market.buy(symbol, self._portfolio.get_stocks_count(symbol))

                # Add the stocks to our portfolio
                self._portfolio.add_stocks(symbol, nb_of_stocks)

                # Calculate the commission
                commission = self._commission.calculate(cost)
                self._bill += commission

                # Adjust the liquidity available
                self._liquidity -= (cost + commission)

                # Validate if we can continue to buy
                # TODO: Add a real function to check if we can still buy stocks
                if self._liquidity <= 0:
                    break

    def run_simulation(self):
        # As long as there is a new business day in our simulation;
        trading = True
        while trading:
            # Sell companies in our portfolio that satisfy our criteria for selling;
            self._sell()

            # If we have enough money, buy companies trading this day that satisfy our criteria for buying;
            # TODO : What is "enough money"?
            if self._liquidity > 0:
                self._buy()

            # Adjust the value of our assets for the day;
            # TODO : Add the draw(), data structure to keep track of value over time & maybe more
            print("{}: {}".format(self._market.get_current_date(),
                                  self._liquidity +
                                  self._portfolio.get_value_of_portfolio(self._market)))

            # Go to the next trading day.
            trading = self._market.next()

