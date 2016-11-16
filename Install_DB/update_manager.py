import requests
import os
import glob
import re
import json
import configparser
import pandas as pd
from datetime import datetime
from time import localtime, strftime
from Manager_DB.DbConnection import DbConnection
from Manager_DB.ManagerCompany import insert_historic_value_to_db, insert_daily_value_to_db, \
                                      insert_dividend_to_db, get_snp500
import sys


def print_message(message):
    """Print a message on the command line. Useful for debugging."""
    line = '--- '
    print(line + message + '\n')


################################################################################################
#
#                                    GET CSVs FROM THE WEB
#
#
################################################################################################


def get_csv(is_fetching_histo=True, is_fetching_daily=True, is_fetching_div=True):
    """Intermediary function in charge of centralizing the fetching of the selected CSVs.

    :param is_fetching_histo: If True, the historical information will be downloaded from MorningStar. Default is True.
    :type is_fetching_histo: bool
    :param is_fetching_daily: If True, the daily information will be downloaded from Yahoo Finance. Default is True.
    :type is_fetching_daily: bool
    :param is_fetching_div: If True, the dividend information will be downloaded from Yahoo Finance. Default is True.
    :type is_fetching_div: bool
    :return: Nothing. All CSVs downloaded will be found in the directory SNP500 located in the project's directory.
    """
    # Get all symbols of the S&P500.
    # TODO: Get all the companies that were in the S&P500 between two dates. Otherwise -> survivor bias.
    # When testing, you might consider lowering the number of companies by slicing this list. ex: add [:50] at the end
    snp500 = get_snp500()

    # Get the configuration file
    config = configparser.ConfigParser()
    config.read('../config.ini')

    # Open the log file for logging the errors that might encounter along the way.
    logfile = open(config.get('path', 'PATH_LOG'), 'a')

    if is_fetching_histo:
        print_message("Fetching the historical data from MorningStar.")
        get_all_historical(snp500, config, logfile)

    if is_fetching_daily:
        print_message("Fetching the daily data from Yahoo Finance.")
        get_all_daily(snp500, config, logfile)

    if is_fetching_div:
        print_message("Fetching the dividend data from Yahoo Finance.")
        get_all_dividend(snp500, config, logfile)

    logfile.close()


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
    """Fetch the CSVs from Yahoo Finance and save the content in a CSV file.

    All CSVs are named following the format: "daily_" + the company's symbol + ".csv"
    ex: For Google, the CSV's name is "daily_GOOGL.csv".

    Log any exceptions raised while querying Yahoo Finance.

    The minimum date that is used when querying Yahoo Finance is written in the configuration file. It can be manually
    adjusted if needed. It is set automatically to the date of the last update after each execution of "installer.py".

    The maximum date that is used when querying Yahoo Finance is the present localtime date.

    :param sp500: List of unique S&P500's companies' symbols.
    :param config: An open configparser
    :param logfile: An open text file used as a log.
    :return: Nothing. All CSVs downloaded will be found in the directory SNP500 located in the project's directory.
    """
    # The months begin with 0. So 0 = January and 11 = December
    day_max = strftime("%d", localtime())
    month_max = strftime("%m", localtime())
    year_max = strftime("%Y", localtime())

    day_min = config.get('daily', 'DAY_MIN')
    month_min = config.get('daily', 'MONTH_MIN')
    year_min = config.get('daily', 'YEAR_MIN')

    dir_path = config.get('path', 'PATH_SNP500')

    prefix = "http://real-chart.finance.yahoo.com/table.csv?s="
    suffix = "&d={}&e={}&f={}&g=d&a={}&b={}&c={}&ignore=.csv".format(month_max, day_max, year_max,
                                                                     month_min, day_min, year_min)

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
    """Fetch the CSVs with dividends only from Yahoo Finance and save the content in a CSV file.

    All CSVs are named following the format: "div_" + the company's symbol + ".csv"
    ex: For Google, the CSV's name is "daily_GOOGL.csv".

    Log any exceptions raised while querying Yahoo Finance.

    The minimum date that is used when querying Yahoo Finance is written in the configuration file. It can be manually
    adjusted if needed. It is set automatically to the date of the last update after each execution of "installer.py".

    The maximum date that is used when querying Yahoo Finance is the present localtime date.

    :param sp500: List of unique S&P500's companies' symbols.
    :param config: An open configparser.
    :param logfile: An open text file used as a log.
    :return: Nothing. All CSVs downloaded will be found in the directory SNP500 located in the project's directory.
    """
    # The months begin with 0. So 0 = January and 11 = December
    day_max = strftime("%d", localtime())
    month_max = strftime("%m", localtime())
    year_max = strftime("%Y", localtime())

    day_min = config.get('dividend', 'DAY_MIN')
    month_min = config.get('dividend', 'MONTH_MIN')
    year_min = config.get('dividend', 'YEAR_MIN')

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
    """Intermediary function in charge of centralizing the update of the database with the downloaded CSVs.

    This function only works if there are files in the directory "SNP500". It should always be called after any of the
    "get" functions. The algorithm requires that the files are named a certain way.

    :param is_updating_histo: If True, the "historical" table will be updated. Default is True.
    :param is_updating_daily: If True, the "daily" table will be updated. Default is True.
    :param is_updating_div: If True, the "dividends" table will be updated. Default is True.
    :return: Nothing. The insertions are made into the database.
    """
    config = configparser.ConfigParser()
    config.read('../config.ini')

    log_path = config.get('path', 'PATH_LOG')
    dir_path = config.get('path', 'PATH_SNP500')

    db = DbConnection(config.get('database', 'HOST'),
                      config.get('database', 'USER'),
                      config.get('database', 'PASSWORD'),
                      config.get('database', 'DATABASE'))

    logfile = open(log_path, 'a')

    # with open(log_path, 'a') as logfile:
    if is_updating_histo:
        print_message("Updating the database with the historical data downloaded.")
        for filename in glob.glob(dir_path + 'histo_*.csv'):
            if os.stat(filename).st_size != 0:
                update_historical(filename, config, logfile, db)
            else:
                logfile.write("{} [UPDATE][HISTO] Skipped \"{}\" because the file was empty.\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))

    if is_updating_daily:
        print_message("Updating the database with the daily data downloaded.")
        for filename in glob.glob(dir_path + 'daily_*.csv'):
            if os.stat(filename).st_size != 0:
                update_daily(filename, config, db)
            else:
                logfile.write("{} [UPDATE][DAILY] Skipped \"{}\" because the file was empty.\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))

    if is_updating_div:
        print_message("Updating the database with the dividend data downloaded.")
        for filename in glob.glob(dir_path + 'div_*.csv'):
            if os.stat(filename).st_size != 0:
                update_dividend(filename, db)
            else:
                logfile.write("{} [UPDATE][DIVID] Skipped \"{}\" because the file was empty.\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))

    logfile.close()


def update_historical(filename, config, logfile, db):
    """Insert in the database the historical financial information for one company.

    This function only works if there are files in the directory "SNP500" with a name like "histo_*.csv", where * is the
    symbol of a company. It should only be called after the function "get_all_historical".

    The function assumes that the first 2 lines of the CSV are the header and that the first column contains the indexes
    of the rows. The column TTM, for Trailing Twelve Months, is excluded; as are any columns where the date isn't in the
    format YYYY-MM. It also excludes a column where all values are Null. It might happen if the company's financial
    information are missing for one year (like if it didn't exist back then).

    :param filename: The full path of the CSV containing the historical information of a company.
    :param config: An open configparser.
    :param logfile: An open text file used as a log.
    :param db: A DBConnection object for the database.
    :return: Nothing. The insertions are made into the table "historic_value" in the database.
    """
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
    # The check for Null is important because the function replace() cannot be used on it. The program would crash.
    histo_funct = {'Revenue USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
                   'Gross Margin %': float,
                   'Net Income USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
                   'Earnings Per Share USD': float,
                   'Dividends USD': float,
                   'Book Value Per Share * USD': float,
                   'Free Cash Flow Per Share * USD': float}
    for row, funct in histo_funct.items():
        df.loc[row] = df.loc[row].apply(funct)

    # For every year (column), we insert its data in the db.
    for col in df.columns.values:
        if reg_expr.match(col) is not None:
            # Converting the NaN values into None for the sql query.
            numerical_param = list(map(lambda n: None if pd.isnull(n) else n, list(df[col].values)))

            # Skipping this column if all values are None
            if all(num is None for num in numerical_param):
                logfile.write("{} [UPDATE][HISTO] Skipping the year {} of the company {}. Data : {}\n"
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), col, symbol, numerical_param))
                continue

            # Converting the date (str) into datetime for the sql query.
            date = pd.to_datetime(col, format='%Y-%m')
            query_params = [datetime(date.year, date.month, date.day)] + numerical_param
            insert_historic_value_to_db(str(symbol), query_params, db)


def update_daily(filename, config, db):
    """Insert in the database the daily stock prices of a company.

    This function only works if there are files in the directory "SNP500" with a name like "daily_*.csv", where * is the
    symbol of a company. It should only be called after the function "get_all_daily".

    :param filename: The full path of the CSV containing the daily stock price information of a company.
    :param config: An open configparser.
    :param db: A DBConnection object for the database.
    :return: Nothing. The insertions are made into the table "daily_value" in the database.
    """
    # Cut the filename to get the symbol of the company; which is always the name of the CSV file.
    basename = os.path.splitext(filename)[0]
    type_and_symbol = basename.rsplit('/', 1)[1]
    symbol = type_and_symbol.rsplit('_', 1)[1]

    df = pd.read_csv(filename)
    daily_values = list(df.columns.values)

    for row in df.itertuples(False):
        date = pd.to_datetime(row[daily_values.index('Date')], format='%Y-%m')

        # Take only the rows that we need. The list containing the names of those rows is in the configuration file.
        numerical_param = []
        for col_name in json.loads(config.get('list', 'DAILY_COL')):
            numerical_param.append(row[daily_values.index(col_name)])
        # All the values are converted to float.
        # (Unless we keep the Volume; which should be an integer. This is not implemented as for now.)
        numerical_param = list(map(lambda n: float(n), numerical_param))
        query_params = [datetime(date.year, date.month, date.day)] + numerical_param
        insert_daily_value_to_db(str(symbol), query_params, db)


def update_dividend(filename, db):
    """Insert in the database each dividend paid by a company and when each transaction was made.

    This function only works if there are files in the directory "SNP500" with a name like "div_*.csv", where * is the
    symbol of a company. It should only be called after the function "get_all_dividend".

    :param filename: The full path of the CSV containing the dividends paid by a company.
    :param db: A DBConnection object for the database.
    :return: Nothing. The insertions are made into the table "dividends" in the database.
    """
    # Cut the filename to get the symbol of the company; which is always the name of the CSV file.
    basename = os.path.splitext(filename)[0]
    type_and_symbol = basename.rsplit('/', 1)[1]
    symbol = type_and_symbol.rsplit('_', 1)[1]

    df = pd.read_csv(filename)
    div_values = list(df.columns.values)

    for row in df.itertuples(False):
        date = pd.to_datetime(row[div_values.index('Date')], format='%Y-%m')
        numerical_param = float(row[div_values.index('Dividends')])
        insert_dividend_to_db(str(symbol), datetime(date.year, date.month, date.day), numerical_param, db)
