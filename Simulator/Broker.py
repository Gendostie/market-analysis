from enum import Enum
from Market import Market

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


def flat_fee_commission(value):
    """Construct an instance of _Commission of the type flat_fee for a type of transaction (buy or sell)

    :param value: The flat fee which is charged for this type of transaction. Must be > 0.
    :type value: float | int
    :return: An instance of _Commission for a flat fee. If value <= 0, there will be no commission.
    :rtype: _Commission
    """
    if value > 0:
        return _Commission(_TypeCommission.flat_fee, value)
    else:
        return _Commission(_TypeCommission.none)


def percent_commission(value):
    """Construct an instance of _Commission of the type percent for a type of transaction (buy or sell)

    :param value: The percent of the transaction value which is charged. Must be > 0 or between ]0,1].
    :type value: float | int
    :return: An instance of _Commission for a percent commission. If value is not valid, there will be no commission.
    :rtype: _Commission
    """
    if 0 < value <= 1:
        return _Commission(_TypeCommission.percent, value)
    elif value > 0:
        return _Commission(_TypeCommission.percent, value/100)
    else:
        return _Commission(_TypeCommission.none)


#########################################################################################################
#                                         Portfolio
#########################################################################################################
class _Portfolio:
    def __init__(self):
        """A portfolio is keeping the number of stocks we own."""
        self.portfolio = {}

    def add_stocks(self, symbol, nb_stocks):
        # TODO: Test for integer
        # TODO: Check if "stocks" is okay
        # TODO: Validate more? Exception? ValueError?
        """Add a certain number of stocks for a company.

        Do nothing if the number of stocks is 0 or less; or if the number of stocks is not an integer.

        :param symbol: Symbol of the stocks' company.
        :type symbol: str
        :param nb_stocks: Number of stocks we want to add for the company. Must be > 0.
        :type nb_stocks: int
        :return: Nothing
        """
        if nb_stocks > 0 and isinstance(nb_stocks, int):
            if symbol in self.portfolio:
                self.portfolio[symbol] += nb_stocks
            else:
                self.portfolio[symbol] = nb_stocks

    def remove_stocks(self, symbol, nb_stocks):
        # TODO: Gérer quand nb_stock > nb dans portfolio
        if nb_stocks > 0:
            if symbol in self.portfolio:
                if nb_stocks < self.portfolio[symbol]:
                    self.portfolio[symbol] -= nb_stocks
                elif nb_stocks == self.portfolio[symbol]:
                    self.portfolio.pop(symbol)

    def get_companies(self):
        """Return a list of the symbol of each company in the portfolio.

        :return: List of the symbol of each company in the portfolio.
        :rtype: list
        """
        return list(self.portfolio.keys())

    def get_value(self, market):
        # TODO: To finish
        """Return how much we could make if we were to sell all of our stocks at the current date.

        :param market: An instance of the class Market
        :return: Market
        """
        stocks_value = 0
        for symbol, nb_stocks in self.portfolio.items():
            stocks_value += nb_stocks * market.get_price(symbol)
        return stocks_value

    # TODO: ONLY FOR DEBUGGING
    def print_portfolio(self):
        for symbol, stocks in self.portfolio.items():
            print("{} -> {}".format(symbol, stocks))


#########################################################################################################
#                                           Broker
#########################################################################################################
class Broker:
    def __init__(self, initial_liquidity,
                 market,
                 sell_commission=_Commission(_TypeCommission.none),
                 buy_commission=_Commission(_TypeCommission.none),):
        self._market = market

        self._liquidity = initial_liquidity
        self._portfolio = _Portfolio()

        self._sell_commission = sell_commission
        self._buy_commission = buy_commission

        # TODO: ONLY FOR TESTING
        print(self._sell_commission.calculate(1000))
        print(self._buy_commission.calculate(1000))
        print(self._portfolio.get_companies())
        print(self._portfolio.get_value(market))

        self._portfolio.add_stocks("A", 100)
        self._portfolio.add_stocks("GOOGL", 200)
        self._portfolio.add_stocks("GE", 1000)
        self._portfolio.add_stocks("ZTS", 10)
        self._portfolio.remove_stocks("ABC", 100)
        self._portfolio.remove_stocks("ZTS", 100)
        self._portfolio.remove_stocks("GOOGL", 100)
        self._portfolio.remove_stocks("A", 100)
        print(self._portfolio.get_companies())
        print(self._portfolio.get_value(market))
        market.next()
        print(self._portfolio.get_value(market))
        market.next()
        print(self._portfolio.get_value(market))

        self._portfolio.print_portfolio()
        # TODO: ONLY FOR TESTING


