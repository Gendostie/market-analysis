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
ROWS_TYPE = {'Revenue USD Mil': lambda x: int(x.replace(",", "")), 'Gross Margin %': float,
             'Net Income USD Mil': lambda x: int(x.replace(",", "")),
             'Earnings Per Share USD': float, 'Dividends USD': float,
             'Book Value Per Share * USD': float, 'Free Cash Flow Per Share * USD': float}

DEBUG = True


def trim_csv(filename):
    """

    :param filename:
    :return:
    """

    db = DBConnection(HOST, USER, PASSWORD, DATABASE)
    reg_expr = re.compile('.{4}-.{2}')

    df = pd.read_csv(filename, header=2, index_col=0)
    df = df.loc[ROWS]

    print(df)

    for row, funct in ROWS_TYPE.items():
        df.loc[row] = df.loc[row].apply(funct)

    for col in df.columns.values:
        if reg_expr.match(col) is not None:
            date = pd.to_datetime(col, format='%Y-%m')
            query_params = [datetime(date.year, date.month, date.day)] + list(df[col].values)
            print(query_params)
            insert_historic_value_to_db("DLR", query_params, db)


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
    with open(LOG_PATH, 'a') as logFile:
        for filename in glob.glob(DIR_PATH + '*.csv'):
            # Make sure that the file is not empty
            if os.stat(filename).st_size != 0:
                trim_csv(filename)
                if DEBUG:
                    break
            elif not DEBUG:
                logFile.write("{} = The file \"{}\" was empty.\n" \
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))
