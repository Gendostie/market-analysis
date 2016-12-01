class Filter:
    def __init__(self, attr=None, value=None):
        self._attr = attr
        self._value = value

    def run(self, lst, market, portfolio):
        return lst


##########################################################################################################
#                                       Test Filters
##########################################################################################################
class FilterPriceGreaterThan(Filter):
    def run(self, lst, market, portfolio):
        new_list = []
        for symbol in lst:
            price = market.get_price(symbol)
            if price > self._value:
                new_list.append(symbol)
        return new_list


class FilterPriceLesserThan(Filter):
    def run(self, lst, market, portfolio):
        new_list = []
        for symbol in lst:
            price = market.get_price(symbol)
            if price <= self._value:
                new_list.append(symbol)
        return new_list


##########################################################################################################
#                                       General Filters
##########################################################################################################
class FilterNot(Filter):
    """SELL: Don't sell any company in our portfolio.  BUY: Don't buy any company."""
    def run(self, lst, market, portfolio):
        return []


##########################################################################################################
#                                         Buy Filters
#                             (keep symbol in list if we want to buy)
##########################################################################################################
class FilterNotInPortfolio(Filter):
    """Only buy companies that we don't have in our portfolio."""
    def run(self, lst, market, portfolio):
        new_list = []
        for symbol in lst:
            nb_stocks = portfolio.get_stocks_count(symbol)
            if nb_stocks == 0:
                new_list.append(symbol)
        return new_list


##########################################################################################################
#                                         Sell Filters
#                             (keep symbol in list if we want to sell)
##########################################################################################################
