class Singleton:
    _instance = None

    class OrderManager:
        def __init__(self):
            self.is_descending = False

    def __init__(self):
        self._instance = self.OrderManager()

    def __new__(cls):
        if not Singleton._instance:
            Singleton._instance = cls.OrderManager()
        return Singleton._instance

    def get_order(self):
        return self.is_descending

    def set_order(self, value):
        self.is_descending = value


def divide(num, denom, mult=1):
    """
    Makes division and multiplied by a factor. Cast the result in string and keep to decimal.
    :param num: numerator of the fraction
    :type num: int | float
    :param denom: denominator of the fraction
    :type denom: int | float
    :param mult: multiplier of the fraction
    :type mult: int | float
    :return: str
    """
    if (num is None) or (denom is None) or (denom == 0):
        return None
    else:
        return "{0:.2f}".format(num/denom*mult)

