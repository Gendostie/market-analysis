from datetime import timedelta


class Market:
    # TODO: To complete in the end
    """Class that encapsulate information about the market between two dates in the past.

    The class is initiated with a starting and ending date. It keeps the current date of the simulation.
    You can go to the next business day with the function next().

    """

    def __init__(self, begin, end, db):
        """

        :param begin:
        :type begin: datetime.datetime
        :param end:
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

    def debug_print(self):
        """For debugging, print df_market"""
        # TODO : REMOVE, only for debugging
        """Print the information for the current date."""
        print(self.df_market.loc[self._current_date])

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
                   WHERE date_daily_value >= "{}"
                     AND date_daily_value <= "{}";""".format(self._current_date, self._end_date)
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
                   WHERE date_daily_value = "{}";""" .format(self._current_date)
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
