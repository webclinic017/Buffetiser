import csv
import json
import os
import shutil
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from control.config import DATA_PATH
from model.data_structures import Config, Share, InvestmentType, Crypto


def validateConfigFile():
    valid = True
    if not os.path.isfile(os.path.join(DATA_PATH, 'config.csv')):
        try:
            # Config doesn't exist so copy example
            s = r'{}/example_config.csv'.format(os.getcwd())
            d = DATA_PATH+'/config.csv'
            if not os.path.isdir(DATA_PATH):
                os.mkdir(DATA_PATH+'/')
            shutil.copyfile(s, d)
        except IOError as e:
            valid = False
        except FileExistsError as error:
            if os.path.isdir(DATA_PATH):
                valid = False
            else:
                print('Unexpected FileExistsError while creating data directory:', error)
                valid = False
        except OSError as error:
            print('Unexpected OSError while creating data directory:', error)
            valid = False

    return valid


def validateInvestmentFile(investmentCode, path):
    valid = False
    if not os.path.isfile(path):
        try:
            with open(path, 'w') as file:
                writeInvestmentDataFile(investmentCode, None)
            valid = True
        except IOError as e:
            pass
        except FileExistsError as error:
            if os.path.isdir(path):
                pass
            else:
                print('Unexpected FileExistsError while creating data directory:', error)
        except OSError as error:
            print('Unexpected OSError while creating data directory:', error)

    return valid


def readConfigFile():

    if not validateConfigFile():
        print('Config file is invalid. Cannot continue.')
        return

    config = Config()
    configPath = os.path.join(DATA_PATH, 'config.csv')
    with open(configPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        for row in csvReader:
            if row[0] == 'dataSupplier':
                config.dataSupplier = row[1]
            elif row[0] == 'dataAccessKey':
                config.dataAccessKey = row[1]
            elif row[0] == 'exchange':
                config.exchange = row[1]
            elif row[0] == 'currency':
                config.currency = row[1]
            elif row[0] == 'currencyConversionKey':
                config.currencyConversionKey = row[1]
            elif row[0] == 'currencyConversion':
                config.currencyConversion = row[1]

    return config


def readPortfolioData(config):

    investmentsHeld = []

    configPath = os.path.join(DATA_PATH, 'config.csv')
    with open(configPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        for row in csvReader:
            if row[0] == 'share':
                investmentsHeld.append(Share(InvestmentType.Share,
                                             1 if config.exchange == 'XASX' else config.currencyConversion,
                                             row[1],
                                             row[2],
                                             row[3],
                                             row[4],
                                             row[5]))
            elif row[0] == 'crypto':
                investmentsHeld.append(Crypto(InvestmentType.Crypto,
                                              config.currencyConversion,
                                              row[1],
                                              row[2],
                                              row[3],
                                              row[4],
                                              row[5]))

    for investment in investmentsHeld:
        if investment.investmentType == InvestmentType.Share:
            investment.priceHistory = readInvestmentDataFile(investment.code)
            investment.setDefaultLivePrice()

    return investmentsHeld


def readInvestmentDataFile(investmentCode):
    path = os.path.join(DATA_PATH, f'data-{investmentCode}.txt')
    validateConfigFile()

    if not os.path.isfile(os.path.join(path)):
        shareHistory = []

        url = 'https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb=' + \
              'au:{}+'.format(investmentCode)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        for entry in soup.findAll('td', {'class': 'symb-col'}):
            symbol = entry.text
            lastPrice = soup.find('td', {'class': 'last-col'}).text
            high = soup.find('td', {'class': 'high-col'}).text
            low = soup.find('td', {'class': 'low-col'}).text
            volume = soup.find('td', {'class': 'volume-col'}).text

            today = datetime.today()
            currentPriceObject = {"date": '{}-{}-{}'.format(today.year, today.month, today.strftime("%d")),
                                  "open": float(low),
                                  "high": float(high),
                                  "low": float(low),
                                  "close": float(lastPrice),
                                  "adjusted_close": float(lastPrice),
                                  "volume": int(volume.replace(',', ''))}
            shareHistory.append(currentPriceObject)

            writeInvestmentDataFile(investmentCode, shareHistory)

    if os.stat(path).st_size == 0:
        print('{} file is empty. Click Live button to add data point.'.format(investmentCode))
        return []
    else:
        with open(path, 'r') as jsonFile:
            shareHistory = json.load(jsonFile)
            return shareHistory


def writeInvestmentDataFile(investmentCode, shareHistory):
    path = os.path.join(DATA_PATH, f'data-{investmentCode}.txt')
    validateInvestmentFile(investmentCode, path)

    shareDataJsonArray = []

    # TODO: fix this up
    if not shareHistory or len(shareHistory) == 0:
        print('Nothing to write')
        return

    # TODO: if date exists in history, update don't add
    for index in range(0, len(shareHistory)):
        shareDataJson = {'date': shareHistory[index]['date'],
                         'high': shareHistory[index]['high'],
                         'low': shareHistory[index]['low'],
                         'close': shareHistory[index]['close']}
        shareDataJsonArray.append(shareDataJson)

    with open(path, 'w') as outfile:
        json.dump(shareDataJsonArray, outfile)


def writeCurrencyConversionValue(currencyConversion):
    """
    Always need a valid currency conversion based on user's currency.
    """
    validateConfigFile()

    configPath = os.path.join(DATA_PATH, 'config.csv')
    outputTempPath = os.path.join(DATA_PATH, 'config-o.csv')
    inFile = open(configPath, 'r')
    reader = csv.reader(inFile, delimiter=',')
    outFile = open(outputTempPath, 'w')
    writer = csv.writer(outFile, delimiter=',')
    for row in reader:
        if row[0] == 'currencyConversion':
            row[1] = currencyConversion
        writer.writerow(row)
    os.rename(outputTempPath, configPath)
