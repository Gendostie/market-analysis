import math


class Portfolio:
    def __init__(self, initial_liquidity, min_value, max_value):
        # TODO : Better comment...
        """A portfolio is keeping the number of stocks we own."""
        self._portfolio = {}
        self._cash = initial_liquidity

        self._min_stock_value = min_value
        self._max_stock_value = max_value

    #######################################################################################################
    #                                Buy/Sell algorithms
    #######################################################################################################

    def maximize_buy(self, symbol, price):
        """Buy as many stocks as possible at a given price for the given company.

        It will not buy for more than the maximum amount set by the user, nor more than it can buy with the
        cash it has. It might leave no margin for the broker's commission though.

        :param symbol: Symbol of the company of which we want to buy stocks.
        :type symbol: str
        :param price: Price at which the stocks of the company are sold in the market.
        :type price: float
        :return: Value of the transaction, which is how much money it cost to buy the stocks. 0 if nothing was done.
        :rtype: float
        """
        # Safety check
        if not self.can_buy() or price <= 0:
            return 0.0

        # Calculate the maximum we can put in $ for this company without busting the maximum set by the user.
        # Formula:= Maximum we can put for one company ($) - Value of stocks we already own for the company ($)
        if symbol in self._portfolio:
            max_value = self._max_stock_value - (self._portfolio[symbol] * price)
        else:
            max_value = self._max_stock_value

        # The maximum value cannot be greater than the cash money we have
        max_value = min(self._cash, max_value)

        # Calculate how many stocks we can buy to max out our investment in this company
        stocks_to_buy = math.floor(max_value / price)

        # Buy the stocks and add them to our portfolio
        cost = stocks_to_buy * price
        if symbol in self._portfolio:
            self._portfolio[symbol] += stocks_to_buy
        else:
            self._portfolio[symbol] = stocks_to_buy

        # Adjust the cash we have after the transaction
        self._cash -= cost

        return cost

    def sell_all_stocks(self, symbol, price):
        """Ask the portfolio to sell all stocks owned for a company at the given price.

        The amount of cash we have is automatically adjusted.

        :param symbol: Symbol of the company which we want to sell all of its stocks that we own.
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

        return gain

    #######################################################################################################
    #                                Information on the portfolio
    #######################################################################################################

    def can_buy(self):
        return self._cash > 0

    def get_stocks_count(self, symbol):
        """Return the number of stocks owned for a company.

        :param symbol: The symbol of the company which we want to know the stocks' count.
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
        :type market: Market
        :return: float
        """
        stocks_value = 0
        for symbol, nb_stocks in self._portfolio.items():
            stocks_value += nb_stocks * market.get_price(symbol)
        return stocks_value

    def get_assets_value(self, market):
        """Return the total of all our assets (cash money available and value of our stocks)

        :param market: An instance of the class Market
        :type market: Market
        :return: float
        """
        return self._cash + self.get_value_of_portfolio(market)

    #######################################################################################################
    #                                         Others
    #######################################################################################################

    def print_portfolio(self):
        # TODO: ONLY FOR DEBUGGING
        for symbol, stocks in self._portfolio.items():
            print("{} -> {}".format(symbol, stocks))
