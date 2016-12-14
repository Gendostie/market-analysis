import random


def get_value_global_ranking(a):
    """
    Function to get value Global ranking to sort list of dict
    :param a: dict company
    :type a: dict
    :return: value of Global Ranking
    :rtype: float
    """
    return float(a.get('Global Ranking', 0))


class Filter:
    def __init__(self, name_attr=None, param1=None, param2=None):
        self._name_attr = name_attr
        self._param1 = param1
        self._param2 = param2

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
            if price > self._param1:
                new_list.append(symbol)
        return new_list


class FilterPriceLesserThan(Filter):
    def run(self, lst, market, portfolio):
        new_list = []
        for symbol in lst:
            price = market.get_price(symbol)
            if price <= self._param1:
                new_list.append(symbol)
        return new_list


class FilterKeepOnlyTen(Filter):
    def run(self, lst, market, portfolio):
        random.shuffle(lst)
        return lst[:10]


class FilterVIP(Filter):
    def run(self, lst, market, portfolio):
        return ["A", "FB", "GOOGL"]


class FilterHistorical(Filter):
    def run(self, lst, market, portfolio):
        for symbol in lst:
            result = market.get_52wk(symbol)
            print("{} is at {}".format(symbol, result))
        return lst


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


class FilterCriteriaMinMaxBuy(Filter):
    """
    Buy company with value of criterion between min value and max value
    _param1 = min_value and _param2 = max_value
    """
    def run(self, lst, market, portfolio):
        fct_criterion_special = {'dividend_yield': market.get_dividend_yield, 'p_e_ratio': market.get_p_e_ratio,
                                'p_b_ratio': market.get_p_b_ratio, '52wk': market.get_52wk}
        new_list = []
        for symbol in lst:
            if self._name_attr in fct_criterion_special.keys():
                value_criterion = fct_criterion_special.get(self._name_attr)(symbol)
            else:
                value_criterion = market.get_value_criterion_company(self._name_attr, symbol)
            if value_criterion is not None and self._param1 > float(value_criterion) > self._param2:
                new_list.append(symbol)
        return new_list


class FilterCriteriaGlobalRankingBuy(Filter):
    def run(self, lst, market, portfolio):
        """
        Calculate Global ranking depending of list criteria for get 100 companies with best global ranking
        :param lst: list of company in market
        :type lst: list[str]
        :param market: object Market
        :type market: Market.Market
        :param portfolio: object Portfolio
        :type portfolio: Portfolio.Portfolio
        :return: list of 100 companies with best global ranking
        :rtype: list[str]
        """
        list_glob_rank_cie = [c.get('symbol') for c in sorted(market.get_list_global_ranking(),
                                                              key=get_value_global_ranking)[:100]]
        if len(list_glob_rank_cie) > 0 and len(lst) > 0:
            # Filter company
            new_list = []
            for company in lst:
                if company in list_glob_rank_cie:
                    new_list.append(company)
            return new_list
        else:
            return lst


##########################################################################################################
#                                         Sell Filters
#                             (keep symbol in list if we want to sell)
##########################################################################################################
class FilterCriteriaMinMaxSell(Filter):
    """
    Sell company with value of criterion more than max value or less than min value
    _param1 = min_value and _param2 = max_value
    """
    def run(self, lst, market, portfolio):
        fct_criterion_special = {'dividend_yield': market.get_dividend_yield, 'p_e_ratio': market.get_p_e_ratio,
                                'p_b_ratio': market.get_p_b_ratio, '52wk': market.get_52wk}
        new_list = []
        for symbol in lst:
            if self._name_attr in fct_criterion_special.keys():
                value_criterion = fct_criterion_special.get(self._name_attr)(symbol)
            else:
                value_criterion = market.get_value_criterion_company(self._name_attr, symbol)
            if value_criterion is not None and self._param1 <= float(value_criterion) <= self._param2:
                new_list.append(symbol)
        return new_list


class FilterCriteriaGlobalRankingSell(Filter):
    def run(self, lst, market, portfolio):
        """
        Calculate Global ranking depending of list criteria for get companies with global ranking not in top 100
        :param lst: list of company in market
        :type lst: list[str]
        :param market: object Market
        :type market: Market.Market
        :param portfolio: object Portfolio
        :type portfolio: Portfolio.Portfolio
        :return: list of companies not in top 100 for global ranking
        :rtype: list[str]
        """
        list_glob_rank_cie = [c.get('symbol') for c in sorted(market.get_list_global_ranking(),
                                                              key=get_value_global_ranking)[:100]]
        if len(list_glob_rank_cie) > 0 and len(lst) > 0:
            # Filter company
            new_list = []
            for company in lst:
                if company in list_glob_rank_cie:
                    new_list.append(company)
            return new_list
        else:
            return lst
