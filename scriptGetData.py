import requests, finsymbols, os
from time import localtime, strftime

DIR_NAME = '/S&P500/'
PATH = os.getcwd() + DIR_NAME
DEBUG = False

if DEBUG:
    os.rename(PATH + 'log.txt', PATH + 'copylog.txt')

# Get all symbols of the S&P500
sp500 = finsymbols.get_sp500_symbols()

# Fetch the CSVs from MorningStar and save the content in a CSV file
prefix = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?&callback=?&t='
suffix = '&region=USA&culture=en-CA&cur=&order=asc'

# Log when we receive nothing for a company
with open(PATH + 'log.txt', 'a') as logFile:
    for i in range(len(sp500)):
        symbol = sp500[i]['symbol']
        company = sp500[i]['company']

        # Replace the '-' by a dot for the URL request
        symbolURL = symbol.replace('-', '.')

        # Try one time to get the CSV. Write in the file if we receive something.
        with open(PATH + symbol + '.csv', 'w') as csvFile:
            csvData = requests.get(prefix + symbolURL + suffix)
            if csvData.text:
                csvFile.write(csvData.text)
            else:
                logFile.write("{} = An empty string was received for {} ({}) \n" \
                              .format(strftime("%d %b %Y %H:%M:%S", localtime()), symbolURL, company))
