class Filter:
    def __init__(self, attr=None, value=None):
        self._attr = attr
        self._value = value

    def run(self, lst, market, portfolio):
        return lst


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


class FilterNot(Filter):
    def run(self, lst, market, portfolio):
        return []

