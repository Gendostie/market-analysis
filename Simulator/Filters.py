def filter1(lst, market, portfolio):
    new_list = []
    for symbol in lst:
        price = market.get_price(symbol)
        if price > 50:
            new_list.append(symbol)
    return new_list


def filter2(lst, market, portfolio):
    new_list = []
    for symbol in lst:
        price = market.get_price(symbol)
        if price <= 100:
            new_list.append(symbol)
    return new_list


def filter3(lst, market, portfolio):
    new_list = []
    for symbol in lst:
        price = market.get_price(symbol)
        if price > 75:
            new_list.append(price)
    return new_list


def fl_not(lst, market, portfolio):
    """Filter that removes all companies in the list."""
    return []
