import math


class Portfolio:
    def __init__(self, initial_liquidity, min_value, max_value, log):
        # TODO : Better comment...
        """
        A portfolio is keeping the number of stocks we own.
        :param initial_liquidity: value to portfolio to begin
        :type initial_liquidity: int
        :param min_value: min stock value to do transaction
        :type min_value: int
        :param max_value: max stock value to invest in a company
        :type max_value: int
        :param log: file to write log
        :type log: file
        """
        self._portfolio = {}

        # Log file to log each transaction
        self.log = log

        # Cash must be an integer between [1, inf[
        # Verification must be done when the user sends input
        self._cash = initial_liquidity

        # Minimum and maximum must be between [0, inf[ and min < max.
        # Verification must be done when the user sends input.
        self._min_stock_value = min_value
        self._max_stock_value = max_value

        # We can set a maximum number of stocks to buy for each companies.
        # Otherwise, it's as many as possible.
        self._max_number_stocks = None

    #######################################################################################################
    #                                Buy/Sell algorithms
    #######################################################################################################

    def get_nb_stocks_to_buy(self, symbol, price):
        # Calculate the maximum we can put in $ for this company without busting the maximum set by the user.
        # Formula:= Maximum we can put for one company ($) - Value of stocks we already own for the company ($)
        if symbol in self._portfolio:
            max_value = self._max_stock_value - (self._portfolio[symbol] * price)
        else:
            max_value = self._max_stock_value

        # The maximum value cannot be greater than the cash money we have
        max_value = min(self._cash, max_value)

        # Calculate how many stocks we can buy to max out our investment in this company
        # Since max_value can be negative and generate negative
        #    number of stocks to buy (which we don't want). We set it to at least 0.
        stocks_to_buy = max(math.floor(max_value / price), 0)

        # If we have a maximum number of stock we can buy for a given transaction,
        # return the minimum between our calculated maximum and the one given by the user.
        if self._max_number_stocks is not None:
            stocks_to_buy = min(stocks_to_buy, self._max_number_stocks)

        return stocks_to_buy

    def buy_stocks(self, symbol, price, date):
        """Buy as many stocks as possible at a given price for the given company.

        It will not buy for more than the maximum amount set by the user, nor more than it can buy with the
        cash it has. That might leave no margin for the broker's commission though.

        The amount of cash we have is automatically adjusted.

        :param symbol: Symbol of the company of which we want to buy stocks.
        :type symbol: str
        :param price: Price at which the stocks of the company are sold in the market.
        :type price: float
        :return: Value of the transaction, which is how much money it cost to buy the stocks. 0 if nothing was done.
        :rtype: float
        """
        # Safety check
        if (not self.can_buy()) or price <= 0:
            return 0.0

        stocks_to_buy = self.get_nb_stocks_to_buy(symbol, price)

        # Buy the stocks and add them to our portfolio
        cost = stocks_to_buy * price

        if cost >= self._min_stock_value:
            if symbol in self._portfolio:
                self._portfolio[symbol] += stocks_to_buy
            else:
                self._portfolio[symbol] = stocks_to_buy

            # Adjust the cash we have after the transaction
            self._cash -= cost

            # Log the transaction
            self.log.write("{};BUY;{};{};{}\n".format(date, symbol, stocks_to_buy, cost))
        else:
            cost = 0.0
        return cost

    def sell_all_stocks(self, symbol, price, date):
        """Ask the portfolio to sell all stocks owned for a company at the given price.

        The amount of cash we have is automatically adjusted.

        :param symbol: Symbol of the company of which we want to sell all of its stocks.
        :type symbol: str
        :param price: The price at which the stocks will be bought in the market.
        :type price: float
        :return: Value of the transaction, which is how much money we made by selling the stocks. 0 if nothing was done.
        :rtype: float
        """
        # Safety check.
        nb_stocks = self.get_stocks_count(symbol)
        if price <= 0 or nb_stocks <= 0:
            return 0.0

        # Sell the stocks and remove them from the portfolio
        gain = nb_stocks * price
        self._portfolio.pop(symbol)

        # Adjust the cash we have after the transaction
        self._cash += gain
        self.log.write("{};SELL;{};{};{}\n".format(date, symbol, nb_stocks, gain))

        return gain

    #######################################################################################################
    #                                Information on the portfolio
    #######################################################################################################

    def can_buy(self):
        # TODO: Better function?
        """Indicate if it is possible to buy stocks to avoid calculating for nothing.

        As for now, only checks if we have at least one cent.

        :return: True if it's possible to buy stocks. False otherwise.
        :rtype: bool
        """
        return self._cash >= self._min_stock_value

    def get_stocks_count(self, symbol):
        """Return the number of stocks owned for a company.

        :param symbol: The symbol of the company for which we want to know the stocks' count.
        :type symbol: str
        :return: Number of stocks owned for the company. 0 if we hold no stocks for this company.
        :rtype: int
        """
        if symbol in self._portfolio:
            return self._portfolio[symbol]
        else:
            return 0

    def get_companies(self):
        """Return a list of the symbol of each company in the portfolio.

        :return: List of the symbol of each company in the portfolio.
        :rtype: list
        """
        return list(self._portfolio.keys())

    #######################################################################################################
    #                                Value of the portfolio
    #######################################################################################################

    def get_value_of_portfolio(self, market):
        """Return how much we could make if we were to sell all of our stocks at the current date.

        :param market: An instance of the class Market
        :type market: Market.Market
        :return: float
        """
        stocks_value = 0.0
        for symbol, nb_stocks in self._portfolio.items():
            stocks_value += nb_stocks * market.get_price(symbol)
        return stocks_value

    def get_cash_money(self):
        return self._cash

    #######################################################################################################
    #                                         Others
    #######################################################################################################

    def set_max_number_of_stocks_to_buy(self, nb_stocks):
        self._max_number_stocks = nb_stocks

    def print_portfolio(self):
        """ONLY FOR DEBUGGING"""
        for symbol, stocks in self._portfolio.items():
            print("{} -> {}".format(symbol, stocks))
