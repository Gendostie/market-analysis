import requests
import finsymbols
import os
import glob
import re
import json
import configparser
import pandas as pd
from datetime import datetime
from time import localtime, strftime
import numpy as np
from Manager_DB.DbConnection import DBConnection
from Manager_DB.ManagerCompany import insert_historic_value_to_db, insert_daily_value_to_db

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


################################################################################################
#
#                                    GET CSV FROM THE WEB
#
#
################################################################################################


# TODO : Add a comment
def get_all_csv(get_histo=True, get_daily=True):
    # Get all symbols of the S&P500
    sp500 = finsymbols.get_sp500_symbols()

    # Get the CSVs from MorningStar for the historical information.
    if get_histo:
        get_all_historical(sp500)

    # Get the CSVs from Yahoo Finance for the daily information.
    if get_daily:
        get_all_daily(sp500)


# TODO : Add a verification to download only what is needed.
def get_all_historical(sp500):
    # Fetch the CSVs from MorningStar and save the content in a CSV file
    prefix = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?&callback=?&t='
    suffix = '&region=USA&culture=en-CA&cur=&order=asc'

    config = configparser.ConfigParser()
    config.read('../config.ini')

    log_path = config.get('path', 'PATH_LOG')
    dir_path = config.get('path', 'PATH_SNP500')

    # Log when we receive nothing for a company
    with open(log_path, 'a') as logFile:
        for i in range(len(sp500)):
            symbol = sp500[i]['symbol']
            company = sp500[i]['company']

            # Replace the '-' by a dot for the URL request
            symbol_url = symbol.replace('-', '.')

            # Try one time to get the CSV. Write in the file if we receive something.
            with open(dir_path + symbol + '.csv', 'w') as csvFile:
                r = requests.get(prefix + "histo_" + symbol_url + suffix)
                if r.text:
                    csvFile.write(r.text)
                else:
                    logFile.write("{} = An empty string was received for {} ({}) \n"
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), symbol_url, company))


def get_all_daily(sp500):
    # Get all the configuration from the config.ini file
    config = configparser.ConfigParser()
    config.read('../config.ini')

    day_max = config.get('daily', 'DAY_MAX')
    month_max = config.get('daily', 'MONTH_MAX')
    year_max = config.get('daily', 'YEAR_MAX')

    day_min = config.get('daily', 'DAY_MIN')
    month_min = config.get('daily', 'MONTH_MIN')
    year_min = config.get('daily', 'YEAR_MIN')

    log_path = config.get('path', 'PATH_LOG')
    dir_path = config.get('path', 'PATH_SNP500')

    # Fetch the CSVs from MorningStar and save the content in a CSV file
    prefix = "http://real-chart.finance.yahoo.com/table.csv?s="
    suffix = "&d={}&e={}&f={}&g=d&a={}&b={}&c={}&ignore=.csv".format(day_max, month_max, year_max,
                                                                     day_min, month_min, year_min)

    # Log when we receive nothing for a company
    # TODO : Add verification that the file is a CSV.
    with open(log_path, 'a') as logFile:
        for i in range(len(sp500)):
            symbol = sp500[i]['symbol']
            company = sp500[i]['company']

            # Try one time to get the CSV. Write in the file if we receive something.
            with open(dir_path + "daily_" + symbol + '.csv', 'w') as csvFile:
                r = requests.get(prefix + symbol + suffix)
                if r.text:
                    csvFile.write(r.text)
                else:
                    logFile.write("{} = An empty string was received for {} ({}) \n"
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), symbol, company))


################################################################################################
#
#                                   SET UP DATABASE FROM SCRATCH
#
#
################################################################################################


# TODO : Add a verification to update only what is needed
def set_up_all_with_csv(set_up_histo=True, set_up_daily=True):
    config = configparser.ConfigParser()
    config.read('../config.ini')

    log_path = config.get('path', 'PATH_LOG')
    dir_path = config.get('path', 'PATH_SNP500')

    db = DBConnection(config.get('database', 'HOST'),
                      config.get('database', 'USER'),
                      config.get('database', 'PASSWORD'),
                      config.get('database', 'DATABASE'))

    with open(log_path, 'a') as logFile:
        # Updating with historical data
        if set_up_histo:
            for filename in glob.glob(dir_path + 'histo_*.csv'):
                # If the file is not empty, call the function in charge of the update.
                if os.stat(filename).st_size != 0:
                    set_up_historical(filename, db)
                else:
                    logFile.write("{} = The file \"{}\" was empty.\n" \
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))

        # Updating with daily data
        if set_up_daily:
            for filename in glob.glob(dir_path + 'daily_*.csv'):
                # If the file is not empty, call the function in charge of the update.
                if os.stat(filename).st_size != 0:
                    set_up_daily(filename, db)
                else:
                    logFile.write("{} = The file \"{}\" was empty.\n" \
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))


def set_up_historical(filename, db):
    """

    :param filename:
    :return:
    """
    config = configparser.ConfigParser()
    config.read('../config.ini')

    log_path = config.get('path', 'PATH_LOG')

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
    with open(log_path, 'a') as log_file:
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


def set_up_daily(filename, db):
    # TODO : Not using the log file
    config = configparser.ConfigParser()
    config.read('../config.ini')

    log_path = config.get('path', 'PATH_LOG')

    # Cut the filename to get the symbol of the company; which is always the name of the CSV file.
    basename = os.path.splitext(filename)[0]
    type_and_symbol = basename.rsplit('/', 1)[1]
    symbol = type_and_symbol.rsplit('_', 1)[1]

    df = pd.read_csv(filename)
    daily_values = list(df.columns.values)

    with open(log_path, 'a') as log_file:
        for row in df.itertuples(False):
            date = pd.to_datetime(row[daily_values.index('Date')], format='%Y-%m')

            numerical_param = []
            for c_name in DAILY_COL:
                numerical_param.append(row[daily_values.index(c_name)])
            numerical_param = list(map(lambda n: int(n) if n == np.int else float(n), numerical_param))

            query_params = [datetime(date.year, date.month, date.day)] + numerical_param
            insert_daily_value_to_db(str(symbol), query_params, db)
