import os, glob
import pandas as p
from time import localtime, strftime

DIR_NAME = '/S&P500/'
DIR_CLEAN = '/Clean/'
PATH = os.getcwd() + DIR_NAME
DEBUG = True
ROWS = ['Revenue USD Mil', 'Gross Margin %', 'Net Income USD Mil', 'Earnings Per Share USD',
        'Dividends USD', 'Book Value Per Share * USD', 'Free Cash Flow Per Share * USD']


def verify_data_frame(filename, cie_data_frame):
    """
    Take a pandas' DataFrame and make sure that we have all the required rows.
    :param filename:
    :param cie_data_frame:
    :return:
    """
    rows_name = cie_data_frame.index
    with open(PATH + 'log.txt', 'a') as log_file:
        for name in ROWS:
            if not (name in rows_name):
                log_file.write("{} = The file \"{}\" was missing the row {}.\n"
                               .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename, name))


def trim_csv(filename):
    """

    :param filename:
    :return:
    """
    csv_data = p.read_csv(filename, header=2, thousands=',', error_bad_lines=False, index_col=0)
    # csv_data.loc[ROWS, :]
    # verify_data_frame(filename, csv_data)
    # print csv_data.loc[ROWS, :]
    # print csv_data.index
    # basename, ext = os.path.splitext(filename)
    # with open(basename + '.new', 'w') as outFile:
    with open(filename, 'w') as outFile:
        csv_data.loc[ROWS, :].to_csv(outFile)


# Main
with open(PATH + 'log.txt', 'a') as logFile:
    for filename in glob.glob(PATH + '*.csv'):
        # Make sure that the file is not empty
        if os.stat(filename).st_size != 0:
            trim_csv(filename)
            if DEBUG:
                break
        elif not DEBUG:
            logFile.write("{} = The file \"{}\" was empty.\n" \
                          .format(strftime("%d %b %Y %H:%M:%S", localtime()), filename))
