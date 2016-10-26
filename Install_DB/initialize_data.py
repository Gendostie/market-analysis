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


################################################################################################
#
#                                    GET CSV FROM THE WEB
#
#
################################################################################################


# TODO : Add a comment
def get_all_csv(get_histo=True, get_daily=True, get_div=True):
    # Get all symbols of the S&P500
    sp500 = finsymbols.get_sp500_symbols()

    # Get the CSVs from MorningStar for the historical information.
    if get_histo:
        get_all_historical(sp500)
#    else:
#        print("MorningStar's CSV were not queried.")

    # Get the CSVs from Yahoo Finance for the daily information.
    if get_daily:
        get_all_daily(sp500)
#    else:
#        print("Yahoo Finance's CSV were not queried.")
    if get_div:
        get_all_dividend(sp500)


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
            with open(dir_path + "histo_" + symbol + '.csv', 'w') as csvFile:
                r = requests.get(prefix + symbol_url + suffix)
                if r.text:
                    csvFile.write(r.text)
                else:
                    logFile.write("{} = An empty string was received for {} ({}) \n"
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), symbol_url, company))


def get_all_daily(sp500):
    # Get all the configuration from the config.ini file
    config = configparser.ConfigParser()
    config.read('../config.ini')

    # day_max = config.get('daily', 'DAY_MAX')
    # month_max = config.get('daily', 'MONTH_MAX')
    # year_max = config.get('daily', 'YEAR_MAX')

    day_max = strftime("%d", localtime())
    month_max = strftime("%m", localtime())
    year_max = strftime("%Y", localtime())

    print("Date max = {}-{}-{}".format(year_max, month_max, day_max))

    day_min = config.get('daily', 'DAY_MIN')
    month_min = config.get('daily', 'MONTH_MIN')
    year_min = config.get('daily', 'YEAR_MIN')

    print("Date min = {}-{}-{}".format(year_min, month_min, day_min))

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

    config['daily']['DAY_MIN'] = day_max
    config['daily']['MONTH_MIN'] = month_max
    config['daily']['YEAR_MIN'] = year_max
    with open('../config.ini', 'w') as configfile:
        config.write(configfile)


def get_all_dividend(sp500):
    # Get all the configuration from the config.ini file
    config = configparser.ConfigParser()
    config.read('../config.ini')

    day_max = strftime("%d", localtime())
    month_max = strftime("%m", localtime())
    year_max = strftime("%Y", localtime())

    day_min = config.get('daily', 'DAY_MIN')
    month_min = config.get('daily', 'MONTH_MIN')
    year_min = config.get('daily', 'YEAR_MIN')

    log_path = config.get('path', 'PATH_LOG')
    dir_path = config.get('path', 'PATH_SNP500')

    # Fetch the CSVs from MorningStar and save the content in a CSV file
    prefix = "http://real-chart.finance.yahoo.com/table.csv?s="
    suffix = "&a={}&b={}&c={}&d={}&e={}&f={}&g=v&ignore=.csv".format(month_min, day_min, year_min,
                                                                     month_max, day_max, year_max)

    # Log when we receive nothing for a company
    # TODO : Add verification that the file is a CSV.
    with open(log_path, 'a') as logFile:
        for i in range(len(sp500)):
            symbol = sp500[i]['symbol']
            company = sp500[i]['company']

            # Try one time to get the CSV. Write in the file if we receive something.
            with open(dir_path + "div_" + symbol + '.csv', 'w') as csvFile:
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
def set_up_all_with_csv(set_histo=True, set_daily=True, set_div=True):
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
        if set_histo:
            for filename in glob.glob(dir_path + 'histo_*.csv'):
                # If the file is not empty, call the function in charge of the update.
                if os.stat(filename).st_size != 0:
                    set_up_historical(filename, db)
                else:
                    logFile.write("{} = The file \"{}\" was empty.\n" \
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))

        # Updating with daily data
        if set_daily:
            for filename in glob.glob(dir_path + 'daily_*.csv'):
                # If the file is not empty, call the function in charge of the update.
                if os.stat(filename).st_size != 0:
                    set_up_daily(filename, db)
                else:
                    logFile.write("{} = The file \"{}\" was empty.\n" \
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))

        # Updating with dividend data
        if set_div:
            for filename in glob.glob(dir_path + 'div_*.csv'):
                # If the file is not empty, call the function in charge of the update.
                if os.stat(filename).st_size != 0:
                    set_up_dividend(filename, db)
                else:
                    logFile.write("{} = The file \"{}\" was empty.\n" \
                                  .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))


def set_up_historical(filename, db):
    """

    :param filename:
    :return:
    """
    histo_funct = {'Revenue USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
                   'Gross Margin %': float,
                   'Net Income USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
                   'Earnings Per Share USD': float,
                   'Dividends USD': float,
                   'Book Value Per Share * USD': float,
                   'Free Cash Flow Per Share * USD': float}

    config = configparser.ConfigParser()
    config.read('../config.ini')

    log_path = config.get('path', 'PATH_LOG')

    # The dates have the format YYYY-MM in the CVSs. We want to remove the TTM and errors if there are any.
    reg_expr = re.compile('.{4}-.{2}')

    df = pd.read_csv(filename, header=2, index_col=0)
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
            for col_name in json.loads(config.get('list', 'DAILY_COL')):
                numerical_param.append(row[daily_values.index(col_name)])
            numerical_param = list(map(lambda n: float(n), numerical_param))

            query_params = [datetime(date.year, date.month, date.day)] + numerical_param
            insert_daily_value_to_db(str(symbol), query_params, db)


def set_up_dividend(filename, db):
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
