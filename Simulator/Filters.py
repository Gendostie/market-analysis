def filter1(lst, market):
    new_list = []
    for symbol in lst:
        price = market.get_price(symbol)
        if price > 50:
            new_list.append(symbol)
    return new_list


def filter2(lst, market):
    new_list = []
    for symbol in lst:
        price = market.get_price(symbol)
        if price <= 100:
            new_list.append(symbol)
    return new_list


def filter3(lst, market):
    new_list = []
    for symbol in lst:
        price = market.get_price(symbol)
        if price > 75:
            new_list.append(price)
    return new_list
