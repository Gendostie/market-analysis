import requests
import finsymbols
import os
import glob
import re
import pandas as pd
from datetime import datetime
from time import localtime, strftime
from Manager_DB.DbConnection import DBConnection
from Manager_DB.ManagerCompany import insert_historic_value_to_db

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'market_analysis'

PATH = os.getcwd()
DIR_PATH = PATH + '/../SNP500/'
LOG_PATH = PATH + '/../log.txt'
DIR_CLEAN_PATH = PATH + '/../Clean/'

ROWS = ['Revenue USD Mil', 'Gross Margin %', 'Net Income USD Mil', 'Earnings Per Share USD',
        'Dividends USD', 'Book Value Per Share * USD', 'Free Cash Flow Per Share * USD']
ROWS_TYPE = {'Revenue USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
             'Gross Margin %': float,
             'Net Income USD Mil': lambda x: None if pd.isnull(x) else int(x.replace(",", "")),
             'Earnings Per Share USD': float,
             'Dividends USD': float,
             'Book Value Per Share * USD': float,
             'Free Cash Flow Per Share * USD': float}

DEBUG = True


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
    for row, funct in ROWS_TYPE.items():
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


def get_all_csv():
    # Get all symbols of the S&P500
    sp500 = finsymbols.get_sp500_symbols()

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


def update_bd_with_csv():
    """ Use all the CSV in the directory SNP500 to update the historical data's table in our database.
    :param: It assumes that we have a ... TODO
    :
    :return: Nothing.
    """

    # Open a database connection
    # TODO : Create a configuration file and fetch the data there.
    db = DBConnection(HOST, USER, PASSWORD, DATABASE)

    # TODO : Remove. Only for testing.
    cpt = 0

    with open(LOG_PATH, 'a') as logFile:
        for filename in glob.glob(DIR_PATH + '*.csv'):
            # If the file is not empty, call the function in charge of the update.
            if os.stat(filename).st_size != 0:
                update_historical(filename, db)

                # TODO : Remove. Only for testing
                cpt += 1
                if DEBUG and (cpt > 505):
                    break

            elif not DEBUG:
                logFile.write("{} = The file \"{}\" was empty.\n" \
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))
