import csv
import os
import requests

from model.data_structures import InvestmentType, Share, Crypto
from view.download_window import DownloadThread
from control.config import DATA_PATH


class Model:
    def __init__(self, fatController):

        self.fatController = fatController
        self.portfolio = []
        self.getCurrentCurrencyConversionRate()

    def getCurrentCurrencyConversionRate(self):
        url = 'https://v6.exchangerate-api.com/v6/' + \
              'da52a4f4e127f7d7c51b87ab' + \
              '/latest/USD'
        response = requests.get(url=url).json()
        self.fatController.currencyConversion = float(response['conversion_rates']['AUD'])
        self.writeCurrencyConversionValue()

    # self.fatController.currencyConversionKey + \

    def createDataFiles(self):
        """
        Need to ensure there are a base set of directories and files.
        :return:
        """

        if not os.path.isfile(os.path.join(DATA_PATH, 'config.csv')):
            try:
                with open(os.path.join(DATA_PATH, 'config.csv'), 'w') as file:
                    print('write stuff')
                    file.write('dataSource')
                    file.write('dataAccessKey,\n')
                    file.write('currency,AUD\n')
                    file.write('Investment Type, Ticker Symbol, Company Name, Units Held, Cost Per Unit, Total Cost\n')
                    file.write('share,AAPL.US,Apple Inc.,1000,20,20000\n')
            except IOError as e:
                pass
            except FileExistsError as error:
                if os.path.isdir(DATA_PATH):
                    pass
                else:
                    print('Unexpected FileExistsError while creating data directory:', error)
            except OSError as error:
                print('Unexpected OSError while creating data directory:', error)

    def portfolioSetup(self):

        self.createDataFiles()

        configPath = os.path.join(DATA_PATH, 'config.csv')
        with open(configPath, 'r') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            for row in csvReader:
                if row[0] == 'dataSupplier':
                    self.fatController.dataSupplier = row[1]
                elif row[0] == 'dataAccessKey':
                    self.fatController.key = row[1]
                elif row[0] == 'exchange':
                    self.fatController.exchange = row[1]
                elif row[0] == 'currency':
                    self.fatController.currency = row[1]
                elif row[0] == 'currencyConversionKey':
                    self.fatController.currencyConversionKey = row[1]
                elif row[0] == 'share':
                    self.portfolio.append(Share(InvestmentType.Share,
                                                self.fatController.currencyConversion,
                                                row[1],
                                                row[2],
                                                row[3],
                                                row[4],
                                                row[5]))
                elif row[0] == 'crypto':
                    self.portfolio.append(Crypto(InvestmentType.Crypto,
                                                 self.fatController.currencyConversion,
                                                 row[1],
                                                 row[2],
                                                 row[3],
                                                 row[4],
                                                 row[5]))

    def readAllLive(self, _):
        self.fatController.downloadThread = DownloadThread(self.fatController)
        self.fatController.downloadThread.downloadingFinished.sig.connect(self.fatController.view.updateAllFields)
        self.fatController.downloadThread.start()

    def calculatePortfolioTotals(self):
        """
        :return: Total sum of all investments for each day for the 100(ish) days.
        """
        portfolioSum = []
        for day in range(0, 255):
            daySum = 0
            for investment in self.portfolio:
                try:
                    daySum += investment.priceHistory['close'][day] * investment.conversion
                except IndexError:
                    pass  # It doesn't matter
            portfolioSum.append(daySum)

        return portfolioSum

    def writeCurrencyConversionValue(self):
        """
        Always need a valid currency conversion based on user's currency.
        """

        configPath = os.path.join(DATA_PATH, 'config.csv')
        outputTempPath = os.path.join(DATA_PATH, 'config-o.csv')
        inFile = open(configPath, 'r')
        reader = csv.reader(inFile, delimiter=',')
        outFile = open(outputTempPath, 'w')
        writer = csv.writer(outFile, delimiter=',')
        for row in reader:
            if row[0] == 'currencyConversion':
                row[1] = self.fatController.currencyConversion
            writer.writerow(row)
        os.rename(outputTempPath, configPath)
