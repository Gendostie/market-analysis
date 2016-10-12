import requests
import finsymbols
import os
import glob
import re
import pandas as pd
from datetime import datetime
from time import localtime, strftime
import numpy as np
from Manager_DB.DbConnection import DBConnection
from Manager_DB.ManagerCompany import insert_historic_value_to_db, insert_daily_value_to_db

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'market_analysis'

PATH = os.getcwd()
DIR_PATH = PATH + '/../SNP500/'
LOG_PATH = PATH + '/../log.txt'

ROWS = ['Revenue USD Mil', 'Gross Margin %', 'Net Income USD Mil', 'Earnings Per Share USD',
        'Dividends USD', 'Book Value Per Share * USD', 'Free Cash Flow Per Share * USD']
HISTO_ROWS = {'Revenue USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
              'Gross Margin %': float,
              'Net Income USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
              'Earnings Per Share USD': float,
              'Dividends USD': float,
              'Book Value Per Share * USD': float,
              'Free Cash Flow Per Share * USD': float}
DAILY_COL = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']

DEBUG = True


def verify_data_frame(filename, cie_data_frame):
    """
    Take a pandas' DataFrame and make sure that we have all the required rows.
    :param filename:
    :param cie_data_frame:
    :return:
    """
    rows_name = cie_data_frame.index
    with open(LOG_PATH, 'a') as log_file:
        for name in ROWS:
            if not (name in rows_name):
                log_file.write("{} = The file \"{}\" was missing the row {}.\n"
                               .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename, name))


# TODO : Add a comment
def get_all_csv():
    # Get all symbols of the S&P500
    sp500 = finsymbols.get_sp500_symbols()

    """
    # Get the CSVs from MorningStar for the historical information.
    get_all_historical(sp500)
    """

    get_all_daily(sp500)


# TODO : Add a verification to download only what is needed.
def get_all_historical(sp500):
    # Fetch the CSVs from MorningStar and save the content in a CSV file
    prefix = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?&callback=?&t='
    suffix = '&region=USA&culture=en-CA&cur=&order=asc'

    # Log when we receive nothing for a company
    with open(LOG_PATH, 'a') as logFile:
        for i in range(len(sp500)):
            symbol = sp500[i]['symbol']
            company = sp500[i]['company']

            # Replace the '-' by a dot for the URL request
            symbol_url = symbol.replace('-', '.')

            # Try one time to get the CSV. Write in the file if we receive something.
            with open(DIR_PATH + symbol + '.csv', 'w') as csvFile:
                r = requests.get(prefix + symbol_url + suffix)
                if r.text:
                    csvFile.write(r.text)
                else:
                    logFile.write("{} = An empty string was received for {} ({}) \n"
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), symbol_url, company))


def get_all_daily(sp500):
    # TODO : Fetch the parameters in a config file.
    day_max = '11'
    month_max = '10'
    year_max = '2016'

    day_min = '01'
    month_min = '01'
    year_min = '2005'

    # Fetch the CSVs from MorningStar and save the content in a CSV file
    prefix = "http://real-chart.finance.yahoo.com/table.csv?s="
    suffix = "&d={}&e={}&f={}&g=d&a={}&b={}&c={}&ignore=.csv".format(day_max, month_max, year_max,
                                                                        day_min, month_min, year_min)

    # Log when we receive nothing for a company
    # TODO : Add verification that the file is a CSV.
    with open(LOG_PATH, 'a') as logFile:
        for i in range(len(sp500)):
            symbol = sp500[i]['symbol']
            company = sp500[i]['company']

            # Try one time to get the CSV. Write in the file if we receive something.
            with open(DIR_PATH + "daily_" + symbol + '.csv', 'w') as csvFile:
                r = requests.get(prefix + symbol + suffix)
                if r.text:
                    csvFile.write(r.text)
                else:
                    logFile.write("{} = An empty string was received for {} ({}) \n"
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), symbol, company))


# TODO : Add a verification to update only what is needed
def update_all_with_csv():
    """ Use all the CSV in the directory SNP500 to update the historical data's table in our database.
    :param: It assumes that we have a ... TODO
    :
    :return: Nothing.
    """

    # TODO : Create a configuration file and fetch the data there.
    db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    with open(LOG_PATH, 'a') as logFile:
        # Updating with historical data
        """
        for filename in glob.glob(DIR_PATH + 'histo_*.csv'):
            # If the file is not empty, call the function in charge of the update.
            if os.stat(filename).st_size != 0:
                update_historical(filename, db)
            else:
                logFile.write("{} = The file \"{}\" was empty.\n" \
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))
        """

        # Updating with daily data
        for filename in glob.glob(DIR_PATH + 'daily_*.csv'):
            # If the file is not empty, call the function in charge of the update.
            if os.stat(filename).st_size != 0:
                update_daily(filename, db)
            else:
                logFile.write("{} = The file \"{}\" was empty.\n" \
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))


def update_historical(filename, db):
    """

    :param filename:
    :return:
    """
    # The dates have the format YYYY-MM in the CVSs. We want to remove the TTM and errors if there are any.
    reg_expr = re.compile('.{4}-.{2}')

    df = pd.read_csv(filename, header=2, index_col=0)
    df = df.loc[ROWS]

    # Cut the filename to get the symbol of the company; which is always the name of the CSV file.
    basename = os.path.splitext(filename)[0]
    symbol = basename.rsplit('/', 1)[1]

    # Since all elements are considered objects, we need to convert them into the type we need for our database.
    # For integers, we also need to remove the comma or it will be interpreted incorrectly.
    # The check for Null is important because the function replace() cannot be used on it. It will crash the program.
    for row, funct in HISTO_ROWS.items():
        df.loc[row] = df.loc[row].apply(funct)

    # For every years (col), we insert its data in the db.
    with open(LOG_PATH, 'a') as log_file:
        for col in df.columns.values:
            if reg_expr.match(col) is not None:
                # Converting the NaN values into None for the sql query.
                numerical_param = list(map(lambda n: None if pd.isnull(n) else n, list(df[col].values)))

                # Skipping this column if all values are None
                if all(num is None for num in numerical_param):
                    log_file.write("{} = Skipping the year {} of the company {}. Data : {}\n"
                                   .format(strftime("%d %b %Y %H:%M:%S", localtime()), col, symbol, numerical_param))
                    continue

                # Converting the date (str) into datetime for the sql query.
                date = pd.to_datetime(col, format='%Y-%m')

                query_params = [datetime(date.year, date.month, date.day)] + numerical_param

                insert_historic_value_to_db(str(symbol), query_params, db)


def update_daily(filename, db):
    # Cut the filename to get the symbol of the company; which is always the name of the CSV file.
    basename = os.path.splitext(filename)[0]
    type_and_symbol = basename.rsplit('/', 1)[1]
    symbol = type_and_symbol.rsplit('_', 1)[1]

    df = pd.read_csv(filename)
    daily_values = list(df.columns.values)

    with open(LOG_PATH, 'a') as log_file:
        for row in df.itertuples(False):
            date = pd.to_datetime(row[daily_values.index('Date')], format='%Y-%m')

            numerical_param = []
            for c_name in DAILY_COL:
                numerical_param.append(row[daily_values.index(c_name)])
            numerical_param = list(map(lambda n: int(n) if n == np.int else float(n), numerical_param))

            query_params = [datetime(date.year, date.month, date.day)] + numerical_param
            insert_daily_value_to_db(str(symbol), query_params, db)


"""
def update_bd_with_yahoo():
    # db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    sp500 = finsymbols.get_sp500_symbols()

    cie_to_do = []
    for i in range(len(sp500) - 400):
        symbol = sp500[i]['symbol'].replace('-', '.')
        cie_to_do.append(symbol)

    with open(LOG_PATH, 'a') as logFile:
        while len(cie_to_do):
            tmp_to_do = []
            timestart = datetime.now()
            for i in cie_to_do:
                # symbol = sp500[i]['symbol'].replace('-', '.')
                # company = sp500[i]['company']

                try:
                    share = Share(i)
                except:
                    tmp_to_do.append(i)

            timestop = datetime.now()
            print("{} companies to do. Skipped {}. It took {}.\n".format(len(cie_to_do), len(tmp_to_do), timestop.timestamp() - timestart.timestamp()))
            print(cie_to_do)
            cie_to_do = list(tmp_to_do)
"""
