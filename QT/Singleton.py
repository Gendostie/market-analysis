class singleton:
    _instance = None

    class order_manager:
        def __init__(self):
            self.is_descending = False

    def __init__(self):
        self._instance = self.order_manager()

    def __new__(cls):
        if not singleton._instance:
            singleton._instance = cls.order_manager()
        return singleton._instance

    def get_order(self):
        return self.is_descending

    def set_order(self, value):
        self.is_descending = value


# TODO: Add comment
def divide(num, denom, mult=1):
    if (num is None) or (denom is None):
        return None
    else:
        return "{0:.2f}".format(num/denom*mult)
