from datetime import datetime, timedelta
from QT.Singleton import divide


class Market:
    """Class that encapsulate information about the market between two dates in the past.

    The class is initiated with a starting and ending date. It keeps the current date of the simulation.
    You can go to the next business day with the function next().

    """

    def __init__(self, begin, end, db):
        """

        :param begin: start date of simulation
        :type begin: datetime.datetime
        :param end: end date of simulation
        :type end: datetime.datetime
        :param db: connexion in to DB
        :type db: Manager_DB.DbConnection.DbConnection
        """
        self._db = db

        # Set the dates for the simulation
        self._current_date = begin
        self._end_date = end

        # Get the list of all business days (must be initialized before any call to __is_business_day() )
        self._business_days = self.__get_business_days()

        # Safety check
        # If the start date given is not a business day, go to the next business day.
        if not self.__is_business_day(begin):
            self.next()

        # Charge the prices for this day. Optimization to speed up the get_price function.
        self._prices = self.__load_prices()

    ####################################################################################################
    #     Callable functions
    ####################################################################################################

    def next(self):
        """Set the date of the market to the next business day.

        This function must be used to go to the next business day of the simulation. It will return
        false if the next day is beyond the simulation's limit. Its only effect is to change the
        state of the object.

        :return: True if the next day is still in the simulation. False if it went beyond the end date.
        :rtype: bool
        """
        if self.__is_over():
            return False
        self._current_date = self._current_date + timedelta(days=1)
        if not self.__is_business_day(self._current_date):
            self.next()
        # Charge the new prices for the day. Optimization to speed up the get_price function.
        self._prices = self.__load_prices()
        return True

    def get_current_date(self):
        """Return the current date of the simulation.

        :rtype: datetime
        """
        return self._current_date

    def get_trading_stocks(self):
        """Return a list of all companies that you can trade for the current date.

        :rtype: list
        """
        return list(self._prices.keys())

    def get_price(self, symbol):
        """Return the closing price of a company for the current day.

        :param symbol: Symbol of the company of which we are requesting the price.
        :type symbol: str
        :return: The "adjusted close" price of the company for the current day. 0 if the company isn't trading that day.
        :rtype: float
        """
        if symbol in self._prices:
            price = self._prices[symbol]
        else:
            price = 0.0
        return price

    def get_value_criterion_company(self, col_name, symbol):
        """
        Return value criterion within col_name of company
        :param col_name: name criterion to get value
        :type col_name: str
        :param symbol: symbol of a company
        :type symbol: str
        :return: value of criterion, if None, return 0.0
        :rtype: float
        """
        query = """SELECT {} FROM historic_value
                    WHERE id_symbol = '{}'
                        AND date_historic_value = (SELECT date_historic_value
                                                      FROM historic_value
                                                      WHERE date_historic_value <= '{}' AND id_symbol = '{}'
                                                    ORDER BY date_historic_value DESC
                                                    LIMIT 1);""".format(col_name, symbol, self._current_date, symbol)

        result = self._db.select_in_db(query)
        if len(result) > 0:
            return result[0][0]
        else:
            return 0.0

    def get_dividend_yield(self, symbol):
        return divide(self.get_value_criterion_company('dividends_usd', symbol),
                      self.get_price(symbol), 100)

    def get_p_e_ratio(self, symbol):
        return divide(self.get_price(symbol),
                      self.get_value_criterion_company('earning_per_share_usd', symbol))

    def get_p_b_ratio(self, symbol):
        return divide(self.get_price(symbol),
                      self.get_value_criterion_company('book_value_per_share_usd', symbol))

    def get_52wk(self, symbol):
        actual_price = self.get_price(symbol)
        # Test if we even need to calculate the 52wk
        if actual_price is None:
            return None

        # If one year before now is before the 3rd of January of 2006, we set it to that date (our min)
        # Check for the dreadful 29th of February...
        if self._current_date.month == 2 and self._current_date.day == 29:
            last_year_date = max(self._current_date.replace(year=self._current_date.year - 1,
                                                            day=self._current_date.day - 1),
                                 datetime(2006, 1, 3))
        else:
            last_year_date = max(self._current_date.replace(year=self._current_date.year - 1),
                                 datetime(2006, 1, 3))

        # Go the the nearest business day (if it isn't already one)
        while not self.__is_business_day(last_year_date):
            last_year_date = last_year_date + timedelta(days=1)

        # Get the price at that date
        query = """SELECT adj_close
                     FROM daily_value
                     WHERE date_daily_value = '{}'
                     AND id_symbol = '{}';""".format(last_year_date, symbol)
        result = self._db.select_in_db(query)
        if result is not ():
            last_year_price = result[0][0]
        else:
            last_year_price = 0

        return divide(actual_price - last_year_price,
                      last_year_price, 100)

    ####################################################################################################
    #     Set up some variables for the simulation
    ####################################################################################################

    def __get_business_days(self):
        """Load a dictionary with all business days of the simulation.

        :return: A dictionary. {Key: Year ; Value: Dict{Key: Month ; Value: List[Business days]}}
        :rtype: dict
        """
        query = """SELECT DISTINCT date_daily_value
                   FROM daily_value
                   WHERE date_daily_value >= '{}'
                     AND date_daily_value <= '{}';""".format(self._current_date, self._end_date)
        business_days = {}
        for tpl in self._db.select_in_db(query):
            date = tpl[0]
            if date.year not in business_days:
                business_days[date.year] = {1: [], 2: [], 3: [], 4: [],
                                            5: [], 6: [], 7: [], 8: [],
                                            9: [], 10: [], 11: [], 12: []}
            business_days[date.year][date.month].append(date.day)
        return business_days

    def __load_prices(self):
        """
        Get adjusted close value of companies in table SQL daily_value
        :return: dict
        """
        dict_prices = {}
        query = """SELECT id_symbol, adj_close
                   FROM daily_value
                   WHERE date_daily_value = '{}';""" .format(self._current_date)
        for symbol, price in self._db.select_in_db(query):
            dict_prices[symbol] = price
        return dict_prices

    ####################################################################################################
    #     Check state of the simulation.
    ####################################################################################################

    def __is_business_day(self, date):
        """Boolean function that verify if a day is a business day.

        Require the initialization of self.business_day with the function get_business_days().

        :param date: The date that we want to check.
        :type date: datetime.datetime
        :return: True if it's a business day. False otherwise.
        :rtype: bool
        """
        if date.year in self._business_days:
            if date.day in self._business_days[date.year][date.month]:
                return True
        return False

    def __is_over(self):
        """Boolean function that verify if the simulation is over.

        :return: True if the current day comes after the ending date. False otherwise.
        :rtype: bool
        """
        if self._current_date.year >= self._end_date.year and \
           self._current_date.month >= self._end_date.month and \
           self._current_date.day >= self._end_date.day:
            return True
        else:
            return False
