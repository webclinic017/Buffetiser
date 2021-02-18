import json
import threading
import os
from datetime import datetime

import requests
from PySide2.QtCore import QObject, Signal, Qt
from PySide2.QtWidgets import QProgressDialog

from model.data_structures import InvestmentType

DATA_PATH = 'data'


class DownloadSignal(QObject):
    sig = Signal(object)


class DownloadThread(threading.Thread):
    downloadingFinished = DownloadSignal()

    def __init__(self, fatController, downloadingWindow, symbol=None):
        threading.Thread.__init__(self)
        self.downloadingWindow = downloadingWindow
        self.fatController = fatController
        self.portfolio = fatController.model.portfolio
        self.symbol = symbol

    def run(self):

        today = datetime.today()
        if self.symbol:
            self.portfolio = [stock.code for stock in self.portfolio if stock.code == self.symbol]
        try:
            os.mkdir(DATA_PATH)
        except FileExistsError as error:
            if os.path.isdir(DATA_PATH):
                pass
            else:
                print('Unexpected FileExistsError while creating data directory:', error)
        except OSError as error:
            print('Unexpected OSError while creating data directory:', error)
        numberOfStocks = len(self.portfolio)
        for count, investment in enumerate(self.portfolio):
            self.downloadingWindow.setLabelText(investment.code)
            if investment.investmentType == InvestmentType.Share:
                # Update historical share data
                self.getShare(today, investment)

            elif investment.investmentType == InvestmentType.Crypto:
                # Update historical crypto data
                self.getCrypto(today, investment)

            self.downloadingWindow.setProgress(((1 + count) / numberOfStocks) * 100)
            self.downloadingFinished.sig.emit(investment)

    def getShare(self, today, investment):
        url = 'https://eodhistoricaldata.com/api/eod/' + \
              investment.code + \
              '.AU?api_token=' + \
              self.fatController.key + \
              '&fmt=json' + \
              '&from={}-{}-{}'.format(today.year - 1, today.month, today.strftime("%d")) + \
              '&to={}-{}-{}'.format(today.year, today.month, today.strftime("%d")) + \
              '&g=m'
        response = requests.get(url=url).json()
        with open(os.path.join(DATA_PATH, f'data-{investment.code}.txt'), 'w') as outfile:
            json.dump(response, outfile)

        # Update current priceHistory
        url = 'https://eodhistoricaldata.com/api/real-time/' + \
              investment.code + \
              '.AU?api_token=' + \
              self.fatController.key + \
              '&fmt=json'
        response = requests.get(url=url).json()
        investment.livePrice = float(response['close'])

    def getCrypto(self, today, investment):
        url = 'https://eodhistoricaldata.com/api/eod/' + \
              investment.code + \
              '-USD.CC?api_token=' + \
              self.fatController.key + \
              '&order=m' + \
              '&fmt=json' + \
              '&from={}-{}-{}'.format(today.year - 1, today.month, today.strftime("%d")) + \
              '&to={}-{}-{}'.format(today.year, today.month, today.strftime("%d")) + \
              '&g=m'

        response = requests.get(url=url).json()
        with open(os.path.join(DATA_PATH, f'data-{investment.code}.txt'), 'w') as outfile:
            json.dump(response, outfile)

        # Update current priceHistory
        url = 'https://eodhistoricaldata.com/api/real-time/' + \
              investment.code + \
              '-USD.CC?api_token=' + \
              self.fatController.key + \
              '&fmt=json'
        response = requests.get(url=url).json()

        url = 'https://www.freeforexapi.com/api/live?pairs=USDAUD'
        self.fatController.usdToAudConversion = float(requests.get(url=url).json()['rates']['USDAUD']['rate'])
        investment.conversion = self.fatController.usdToAudConversion

        price = response['close'] if response['close'] != 'NA' else investment.priceHistory['close'][-1]
        investment.livePrice = float(price)  # in USD


class DownloadWindow(QProgressDialog):
    def __init__(self, parent=None):
        QProgressDialog.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setGeometry(300, 300, 300, 50)

    def setProgress(self, value):
        if value >= 100:
            value = 100
        self.setValue(value)
