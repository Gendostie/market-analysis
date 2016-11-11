import pandas as pd
from datetime import timedelta


class Market:
    """Class that encapsulate information about the market between two dates in the past.

    The class is initiated with a starting and ending date. It keeps the current date of the simulation.
    You can go to the next business day with the function next().

    """
    def __init__(self, begin, end, db):
        self.db = db

        # Set the dates for the simulation
        self.current_date = begin
        self.end_date = end

        # Get the list of all business days
        self.business_days = self.get_business_days()

        # Charge the data for the first day
        self.df_market = self.__load_all_data()

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
            # print("OVER at {} with end date: {}\n".format(self.current_date, self.end_date))
            return False
        self.current_date = self.current_date + timedelta(days=1)
        if not self.__is_business_day(self.current_date):
            self.next()
        return True

    def debug_print(self):
        # TODO : REMOVE, only for debugging
        """Print the information for the current date."""
        print(self.df_market.loc[self.df_market['date'] == self.current_date])

    def get_current_date(self):
        """Return the current date of the simulation."""
        return self.current_date

    ####################################################################################################
    #     Set up some variables for the simulation
    ####################################################################################################
    def __load_all_data(self):
        # TODO: Take a lot of time.
        """Load the daily information of the database in a DataFrame (pandas's object).

        The starting and ending dates are defined when the object is initialized and cannot be changed
        afterward.

        The columns are 'date', 'symbol', 'close' and 'adj_close' (for the adjusted close).

        :return: A Dataframe with all the information from starting date to ending date.
        :rtype: pandas.DataFrame
        """
        query = """SELECT date_daily_value, id_symbol, close_val, adj_close
                   FROM daily_value
                   WHERE date_daily_value >= "{}"
                   AND date_daily_value <= "{}";"""\
            .format(self.current_date, self.end_date)
        list_results = []
        for date, symbol, close, adj_close in self.db.select_in_db(query):
            list_results.append({'date': date, 'symbol': symbol, 'close': close, 'adj_close': adj_close})

        return pd.DataFrame.from_dict(list_results)

    def get_business_days(self):
        """Load a dictionary with all business days of the simulation.

        :return: A dictionary. {Key: Year ; Value: Dict{Key: Month ; Value: List[Business days]}}
        :rtype: dict
        """
        query = """SELECT DISTINCT date_daily_value
                   FROM daily_value
                   WHERE date_daily_value >= "{}"
                     AND date_daily_value <= "{}";""".format(self.current_date, self.end_date)
        business_days = {}
        for tpl in self.db.select_in_db(query):
            date = tpl[0]
            if date.year not in business_days:
                business_days[date.year] = {1: [], 2: [], 3: [], 4: [],
                                            5: [], 6: [], 7: [], 8: [],
                                            9: [], 10: [], 11: [], 12: []}
            business_days[date.year][date.month].append(date.day)
        return business_days

    ####################################################################################################
    #     Check state of the simulation.
    ####################################################################################################
    def __is_business_day(self, date):
        """Boolean function that verify if a day is a business day.

        Require the initialization of self.business_day with the function get_business_days().

        :param date: The date that we want to check.
        :type date: datetime
        :return: True if it's a business day. False otherwise.
        :rtype: bool
        """
        if date.year in self.business_days:
            if date.day in self.business_days[date.year][date.month]:
                return True
        return False

    def __is_over(self):
        """Boolean function that verify is the simulation is over.

        :return: True if the current day comes after the ending date. False otherwise.
        :rtype: bool
        """
        if self.current_date.year > self.end_date.year and\
           self.current_date.month > self.end_date.month and\
           self.current_date.day > self.end_date.day:
            return True
        else:
            return False

