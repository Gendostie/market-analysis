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
from Manager_DB.DbConnection import DBConnection
from Manager_DB.ManagerCompany import insert_historic_value_to_db, insert_daily_value_to_db, insert_dividend_to_db
import sys


################################################################################################
#
#                                    GET CSVs FROM THE WEB
#
#
################################################################################################


def get_csv(is_fetching_histo=True, is_fetching_daily=True, is_fetching_div=True):
    """Intermediary function in charge of centralizing the fetching of the selected CSVs.

    :param is_fetching_histo: If True, the historical information will be downloaded from MorningStar. Default is True.
    :param is_fetching_daily: If True, the daily information will be downloaded from Yahoo Finance. Default is True.
    :param is_fetching_div: If True, the dividend information will be downloaded from Yahoo Finance. Default is True.
    :return: Nothing. All CSVs downloaded will be found in the directory SNP500 located in the project's directory.
    """
    # Get all symbols of the S&P500.
    # TODO: Get all the companies that were in the S&P500 between two dates. Survivor bias.
    sp500 = finsymbols.get_sp500_symbols()

    # Get the configuration file
    config = configparser.ConfigParser()
    config.read('../config.ini')

    # Open the log file for logging the errors that might encounter along the way.
    logfile = open(config.get('path', 'PATH_LOG'), 'a')

    if is_fetching_histo:
        get_all_historical(sp500, config, logfile)

    if is_fetching_daily:
        get_all_daily(sp500, config, logfile)

    if is_fetching_div:
        get_all_dividend(sp500, config, logfile)

    logfile.close()
    # TODO : Any update to do to config?


def get_all_historical(sp500, config, logfile):
    """Fetch the CSVs from MorningStar and save the content in a CSV file.

    All CSVs are named following the format: "histo_" + the company's symbol + ".csv"
    ex: For Google, the CSV's name is "histo_GOOGL.csv".

    Log any exceptions raised while querying MorningStar.

    :param sp500: List of unique S&P500's companies' symbols.
    :param config: An open configparser
    :param logfile: An open text file used as a log.
    :return: Nothing. All CSVs downloaded will be found in the directory SNP500 located in the project's directory.
    """
    prefix = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?&callback=?&t='
    suffix = '&region=USA&culture=en-CA&cur=&order=asc'

    dir_path = config.get('path', 'PATH_SNP500')

    for i in range(len(sp500)):
        symbol = sp500[i]['symbol']
        company = sp500[i]['company']

        # Replace the '-' by a dot for the URL request
        symbol_url = symbol.replace('-', '.')

        with open(dir_path + "histo_" + symbol + '.csv', 'w') as csvFile:
            try:
                r = requests.get(prefix + symbol_url + suffix)
            except:
                logfile.write("{} [FETCH][HISTO] Unexpected error for {} ({}): {} {}\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), symbol, company,
                                      sys.exc_info()[0], sys.exc_info()[1]))

            # In the case that we receive an empty file (quite possible actually), we don't want to overwrite an
            #     existing file containing information.
            if r.text:
                csvFile.write(r.text)


def get_all_daily(sp500, config, logfile):
    # TODO: Data max and min
    """Fetch the CSVs from Yahoo Finance and save the content in a CSV file.

    All CSVs are named following the format: "daily_" + the company's symbol + ".csv"
    ex: For Google, the CSV's name is "daily_GOOGL.csv".

    Log any exceptions raised while querying Yahoo Finance.

    :param sp500: List of unique S&P500's companies' symbols.
    :param config: An open configparser
    :param logfile: An open text file used as a log.
    :return: Nothing. All CSVs downloaded will be found in the directory SNP500 located in the project's directory.
    """
    day_max = config.get('daily', 'DAY_MAX')
    month_max = config.get('daily', 'MONTH_MAX')
    year_max = config.get('daily', 'YEAR_MAX')

    day_min = config.get('daily', 'DAY_MIN')
    month_min = config.get('daily', 'MONTH_MIN')
    year_min = config.get('daily', 'YEAR_MIN')

    dir_path = config.get('path', 'PATH_SNP500')

    prefix = "http://real-chart.finance.yahoo.com/table.csv?s="
    suffix = "&d={}&e={}&f={}&g=d&a={}&b={}&c={}&ignore=.csv".format(day_max, month_max, year_max,
                                                                     day_min, month_min, year_min)

    for i in range(len(sp500)):
        symbol = sp500[i]['symbol']
        company = sp500[i]['company']

        with open(dir_path + "daily_" + symbol + '.csv', 'w') as csvFile:
            try:
                r = requests.get(prefix + symbol + suffix)
            except:
                logfile.write("{} [FETCH][DAILY] Unexpected error for {} ({}): {} {}\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), symbol, company,
                                      sys.exc_info()[0], sys.exc_info()[1]))

            # In the case that we receive an empty file, we don't want to overwrite an existing file
            #      containing information.
            if r.text:
                csvFile.write(r.text)


def get_all_dividend(sp500, config, logfile):
    # TODO: Data max and min
    """Fetch the CSVs from Yahoo Finance and save the content in a CSV file.

    All CSVs are named following the format: "div_" + the company's symbol + ".csv"
    ex: For Google, the CSV's name is "daily_GOOGL.csv".

    Log any exceptions raised while querying Yahoo Finance.

    :param sp500: List of unique S&P500's companies' symbols.
    :param config: An open configparser
    :param logfile: An open text file used as a log.
    :return: Nothing. All CSVs downloaded will be found in the directory SNP500 located in the project's directory.
    """
    day_max = config.get('daily', 'DAY_MAX')
    month_max = config.get('daily', 'MONTH_MAX')
    year_max = config.get('daily', 'YEAR_MAX')

    day_min = config.get('daily', 'DAY_MIN')
    month_min = config.get('daily', 'MONTH_MIN')
    year_min = config.get('daily', 'YEAR_MIN')

    dir_path = config.get('path', 'PATH_SNP500')

    prefix = "http://real-chart.finance.yahoo.com/table.csv?s="
    suffix = "&a={}&b={}&c={}&d={}&e={}&f={}&g=v&ignore=.csv".format(month_min, day_min, year_min,
                                                                     month_max, day_max, year_max)

    for i in range(len(sp500)):
        symbol = sp500[i]['symbol']
        company = sp500[i]['company']

        with open(dir_path + "div_" + symbol + '.csv', 'w') as csvFile:
            try:
                r = requests.get(prefix + symbol + suffix)
            except:
                logfile.write("{} [FETCH][DIVID] Unexpected error for {} ({}): {} {}\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), symbol, company,
                                      sys.exc_info()[0], sys.exc_info()[1]))

            # In the case that we receive an empty file, we don't want to overwrite an existing file
            #      containing information.
            if r.text:
                csvFile.write(r.text)


################################################################################################
#
#                                   UPDATE DATABASE WITH THE CSVs
#
#
################################################################################################


def update_with_csv(is_updating_histo=True, is_updating_daily=True, is_updating_div=True):
    config = configparser.ConfigParser()
    config.read('../config.ini')

    log_path = config.get('path', 'PATH_LOG')
    dir_path = config.get('path', 'PATH_SNP500')

    db = DBConnection(config.get('database', 'HOST'),
                      config.get('database', 'USER'),
                      config.get('database', 'PASSWORD'),
                      config.get('database', 'DATABASE'))

    logfile = open(log_path, 'a')

    # with open(log_path, 'a') as logfile:
    if is_updating_histo:
        for filename in glob.glob(dir_path + 'histo_*.csv'):
            if os.stat(filename).st_size != 0:
                update_historical(filename, config, db)
            else:
                logfile.write("{} [UPDATE][HISTO] Skipped \"{}\" because the file was empty.\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))

    if is_updating_daily:
        for filename in glob.glob(dir_path + 'daily_*.csv'):
            if os.stat(filename).st_size != 0:
                update_daily(filename, db)
            else:
                logfile.write("{} [UPDATE][DAILY] Skipped \"{}\" because the file was empty.\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))

    if is_updating_div:
        for filename in glob.glob(dir_path + 'div_*.csv'):
            if os.stat(filename).st_size != 0:
                update_dividend(filename, db)
            else:
                logfile.write("{} [UPDATE][DIVID] Skipped \"{}\" because the file was empty.\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))

    logfile.close()


def update_historical(filename, config, db):
    histo_funct = {'Revenue USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
                   'Gross Margin %': float,
                   'Net Income USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
                   'Earnings Per Share USD': float,
                   'Dividends USD': float,
                   'Book Value Per Share * USD': float,
                   'Free Cash Flow Per Share * USD': float}

    log_path = config.get('path', 'PATH_LOG')

    # The dates have the format YYYY-MM in the CVSs. We want to remove the TTM and errors if there are any.
    reg_expr = re.compile('.{4}-.{2}')

    df = pd.read_csv(filename, header=2, index_col=0)

    # Take only the rows that we need. The list containing the names of those rows is in the configuration file.
    df = df.loc[json.loads(config.get('list', 'HISTO_ROWS'))]

    # Cut the filename to get the symbol of the company; which is always the name of the CSV file.
    basename = os.path.splitext(filename)[0]
    type_and_symbol = basename.rsplit('/', 1)[1]
    symbol = type_and_symbol.rsplit('_', 1)[1]

    # Since all elements are considered objects, we need to convert them into the type we need for our database.
    # For integers, we also need to remove the comma or it will be interpreted incorrectly.
    # The check for Null is important because the function replace() cannot be used on it. It will crash the program.
    for row, funct in histo_funct.items():
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


def update_daily(filename, db):
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
            for col_name in json.loads(config.get('list', 'DAILY_COL')):
                numerical_param.append(row[daily_values.index(col_name)])
            numerical_param = list(map(lambda n: float(n), numerical_param))

            query_params = [datetime(date.year, date.month, date.day)] + numerical_param
            insert_daily_value_to_db(str(symbol), query_params, db)


def update_dividend(filename, db):
    # TODO : Not using the log file
    config = configparser.ConfigParser()
    config.read('../config.ini')

    log_path = config.get('path', 'PATH_LOG')

    # Cut the filename to get the symbol of the company; which is always the name of the CSV file.
    basename = os.path.splitext(filename)[0]
    type_and_symbol = basename.rsplit('/', 1)[1]
    symbol = type_and_symbol.rsplit('_', 1)[1]

    df = pd.read_csv(filename)
    div_values = list(df.columns.values)

    with open(log_path, 'a') as log_file:
        for row in df.itertuples(False):
            date = pd.to_datetime(row[div_values.index('Date')], format='%Y-%m')

            numerical_param = float(row[div_values.index('Dividends')])

            insert_dividend_to_db(str(symbol), datetime(date.year, date.month, date.day), numerical_param, db)
