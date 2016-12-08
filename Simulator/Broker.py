import random
from datetime import datetime

from Portfolio import Portfolio
from Market import Market
import Filters
import HelperFunctionQt

list_type_simulation = ['technical_analysis', 'by_low_set_high', 'global_ranking', '1_stock_for_each_company']


#########################################################################################################
#                                           Broker
#########################################################################################################
class Broker:
    def __init__(self, db, initial_liquidity, log_broker, log_port,
                 min_date=datetime(2006, 1, 3), max_date=datetime(2016, 11, 4),
                 min_value=0, max_value=float("inf"), fig=None, data_ref_curve=None):
        # TODO: Add comment
        """
        Create Broker
        :param db: connexion in to DB
        :type db: Manager_DB.DbConnection.DbConnection
        :param initial_liquidity: value to portfolio to begin
        :type initial_liquidity: int
        :param log_broker: path file to write log of Broker
        :type log_broker: str
        :param log_port: path file to write log of Portfolio
        :type log_port: str
        :param min_date: date to start simulation
        :type min_date: datetime.datetime
        :param max_date: date included when the simulation stops
        :type max_date: datetime.datetime
        :param min_value: min stock value to do transaction
        :type min_value: int
        :param max_value: max stock value to invest in a company
        :type max_value: int
        :param fig: figure for update plot QT
        :type fig: matplotlib.figure.Figure
        :param data_ref_curve: Data of reference curve for plot Qt simulation
        :type data_ref_curve: pandas.DataFrame
        """
        # The Market where the broker is buying and selling stocks
        self._market = Market(min_date, max_date, db)

        self.log_broker = open(log_broker, 'w')
        self.log_broker.write("date;cash;stocks_value;bill\n")

        # The portfolio contains all the stocks bought for the current day and time and
        # the cash money that can be used instantly by the broker to buy stocks.
        self._portfolio = Portfolio(initial_liquidity, min_value, max_value, log_port)

        # The bill is how much the broker has charged for its services.
        # TODO : Make something of it
        self._bill = 0.0

        # Dictionary that keeps track of the value of our portfolio at any given time since the start of the simulation.
        # Key: Date ; Value: Total of our assets for any given
        self._hist_market_value = {}

        # A commission is how much the broker is asking to get paid for a given transaction.
        # Initially, there is no commission. It must be added with a setter.
        self._commission = self._Commission()

        # Filters are functions used to select which companies should be in our portfolio at any given time.
        self._sell_filters = []
        self._buy_filters = []

        self._fig = fig
        self._data_ref_curve = data_ref_curve

    #######################################################################################################
    #                                      Commission
    #######################################################################################################

    class _Commission:
        def __init__(self, type_commission="no_commission", commission_val=0):
            """Represent a commission charged by the broker to execute a transaction.

            An instance of _Commission should always be created by one of the two functions
            set_flat_fee_commission() and set_percent_commission().

            :param type_commission: "percent", "flat_fee" or "no_commission". Default is "no_commission"
            :type type_commission: str
            :param commission_val: The value of the commission. In % or $ depending of its type.
            :type commission_val: float | int
            :return: None
            """
            self.value = commission_val
            self.type = type_commission

        def calculate(self, transaction_value):
            """Calculate the commission that the broker should charge to the client for the transaction.

            :param transaction_value: The value in $ of the transaction made (buy or sell)
            :type transaction_value: float | int
            :return: The commission that should be charged by the broker for this transaction.
            :rtype: float | int
            """
            return {"percent": transaction_value * self.value,
                    "flat_fee": self.value,
                    "no_commission": 0.0
                    }[self.type]

    #######################################################################################################
    #                                         Setters
    #######################################################################################################
    def set_flat_fee_commission(self, value):
        """Set the commission of the broker to a flat fee for any transaction done.

        :param value: The flat fee that will be charged for any transaction. Must be > 0.
                      If == 0, put to no_commission.
        :type value: float | int
        :return: None
        """
        if value > 0:
            self._commission = self._Commission("flat_fee", value)
        else:
            self._commission = self._Commission()

    def set_percent_commission(self, value):
        """Set the commission of the broker to a percentage of any transaction done.

        :param value: Percentage of the transaction that will be charged. Must be > 0 and < 100.
                      If == 0, put to no_commission.
        :type value: float | int
        :return: None
        """
        if value > 0:
            self._commission = self._Commission("percent", value)
        else:
            self._commission = self._Commission()

    def add_sell_filters(self, *filters):
        """Add one or many filters to reduce the list of companies in our portfolio.

        Functions are regrouped in "Filters.py". They must take as parameters a list of strings, an
        object "Market" and an object "Portfolio".
        The list contains all symbols of the companies in our portfolio that will be sold.
        The "Market" is an instance of the class "Market"; ditto for "Portfolio".

        The filter function must return the same type of list as the one in the parameters. It should be
        reduced to remove all companies in our portfolio that we want to keep because they satisfy a
        specific criterion (or many criteria).

        :param filters: One or many functions as described above.
        :return: None
        """
        for f in filters:
            self._sell_filters.append(f)

    def add_buy_filters(self, *filters):
        """Add one or many filters to reduce the list of companies where we should invest.

        Functions are regrouped in "Filters.py". They must take as parameters a list of strings, an
        object "Market" and an object "Portfolio".
        The list contains all symbols of the companies in our portfolio that will be sold.
        The "Market" is an instance of the class "Market"; ditto for "Portfolio".

        The function must return the same type of list as the one in the parameters. It should be reduced
        to remove all companies where we don't want to invest because they don't satisfy a specific
        criterion (or many criteria).

        :param filters: One or many functions as described above.
        :return: None
        """
        for f in filters:
            self._buy_filters.append(f)

    def add_max_nb_of_stocks_to_buy(self, nb_stocks):
        self._portfolio.set_max_number_of_stocks_to_buy(nb_stocks)

    def set_simulation_predefined(self, type_simulation):
        """
        Set simulation predefined in list_type_simulation
        :param type_simulation: name simulation, if not exists in list_type_simulation do nothing
        :type type_simulation: str
        :return: None
        """
        if type_simulation == list_type_simulation[0]:  # technical_analysis
            print('Configuration technical_analysis')
        if type_simulation == list_type_simulation[1]:  # by_low_set_high
            print('Configuration by_low_set_high')
        if type_simulation == list_type_simulation[2]:  # global_ranking
            print('Configuration global_ranking')
        elif type_simulation == list_type_simulation[3]:  # 1_stock_for_each_company
            self.add_max_nb_of_stocks_to_buy(1)
            self._sell_filters.append(Filters.FilterNot())
            self._buy_filters.append(Filters.FilterNotInPortfolio())
        else:
            return

    #######################################################################################################
    #                                Run the simulation
    #######################################################################################################
    def _sell(self):
        # TODO : Comment
        """
        Sell company
        :return: None
        """
        # Get the list of all companies that we can sell (those we have in our portfolio);
        lst = self._portfolio.get_companies()

        # Filter the list to only keep the companies that should be sold;
        for f in self._sell_filters:
            lst = f.run(lst, self._market, self._portfolio)

        # For all companies that we should sell, sell 'em;
        for symbol in lst:
            # Instruct the portfolio to sell all stocks it has for this company
            gain = self._portfolio.sell_all_stocks(symbol, self._market.get_price(symbol),
                                                   self._market.get_current_date())

            # If it succeeded, calculate the commission
            if gain > 0:
                commission = self._commission.calculate(gain)
                self._bill += commission

    def _buy(self):
        # TODO: Comment
        """
        Buy company
        :return: None
        """
        # Get the list of all companies that we can buy (those trading that day in the market);
        lst = self._market.get_trading_stocks()

        # Filter the list to only keep the companies that we should buy;
        # TODO : Remove those that we already have and which are maxed out.
        for f in self._buy_filters:
            lst = f.run(lst, self._market, self._portfolio)

        # For all companies that we should buy, as long as we have money, buy 'em (random order)
        random.shuffle(lst)
        for symbol in lst:
            # Attempt to buy as many stocks as possible for this company
            # TODO : Allow to choose a different algorithm for buying
            cost = self._portfolio.buy_stocks(symbol, self._market.get_price(symbol),
                                              self._market.get_current_date())

            # If it succeeded, calculate the commission
            if cost > 0:
                commission = self._commission.calculate(cost)
                self._bill += commission

            # Validate if we can continue to buy
            if not self._portfolio.can_buy():
                break

    def _tracking(self, mode_debug=False):
        """
        Log transaction of day
        :param mode_debug: if want print the logs
        :type mode_debug: bool
        :return: None
        """
        # TODO : Add the draw(), data structure to keep track of value over time & maybe more
        # Calculate how much we have
        # TODO : Remove bill?
        self._hist_market_value[self._market.get_current_date()] = \
            self._portfolio.get_cash_money() + \
            self._portfolio.get_value_of_portfolio(self._market) -\
            self._bill
        if mode_debug:
            print("{}\t\t{}".format(self._market.get_current_date(),
                                    self._hist_market_value[self._market.get_current_date()]))
        self.log_broker.write("{};{};{};{}\n".format(self._market.get_current_date(),
                                                     self._portfolio.get_cash_money(),
                                                     self._portfolio.get_value_of_portfolio(self._market),
                                                     self._bill))

    def run_simulation(self, mode_debug=False):
        """
        Start simulation
        :param mode_debug: if want print the logs
        :type mode_debug: bool
        :return: None
        """
        # As long as there is a new business day in our simulation;
        trading = True
        cpt_update_plot_qt = 0
        while trading:
            # Sell companies in our portfolio that satisfy our criteria for selling;
            self._sell()

            # If we have enough money, buy companies trading this day that satisfy our criteria for buying;
            if self._portfolio.can_buy():
                self._buy()

            # Keep track of our assets
            self._tracking(mode_debug)
            # Update plot QT
            if self._fig and cpt_update_plot_qt >= 20:
                HelperFunctionQt.update_plot(self._fig, list(self._hist_market_value.keys()),
                                             list(self._hist_market_value.values()), self._data_ref_curve)
                cpt_update_plot_qt = 0
            else:
                cpt_update_plot_qt += 1

            # Go to the next trading day.
            trading = self._market.next()
        # Update plot QT
        if self._fig:
            HelperFunctionQt.update_plot(self._fig, list(self._hist_market_value.keys()),
                                         list(self._hist_market_value.values()), self._data_ref_curve)
        # TODO: Remove this print, instead, print a summarize in the log.
        if mode_debug:
            self._portfolio.print_portfolio()
