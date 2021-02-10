import threading
from datetime import datetime

import requests
from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QProgressDialog

from model.data_handlers import getTickerData


class DownloadSignal(QObject):
    sig = Signal()


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

        numberOfStocks = len(self.portfolio)
        for count, stock in enumerate(self.portfolio):
            # Update historical data
            url = 'https://eodhistoricaldata.com/api/eod/' + \
                  stock.code + \
                  '.AU?api_token=' + \
                  self.fatController.key + \
                  '&fmt=json' + \
                  '&from=' + str(today.year-1) + '-' + str(today.month) + '-' + today.strftime("%d") + \
                  '&to=' + str(today.year) + '-' + str(today.month) + '-' + today.strftime("%d") + \
                  '&g=m'
            response = requests.get(url=url).json()
            with open('data/data-{}.txt'.format(stock.code), 'w') as outfile:
                json.dump(response, outfile)

            # Update current prices
            url = 'https://eodhistoricaldata.com/api/real-time/' + \
                  stock.code + \
                  '.AU?api_token=' + \
                  self.fatController.key + \
                  '&fmt=json'
            response = requests.get(url=url).json()
            stock.currentPrice = response['close']
            print('{} {}'.format(stock.code, stock.currentPrice))
            self.downloadingWindow.setProgress(((1 + count) / numberOfStocks) * 100)
            self.downloadingWindow.setLabelText(stock.code)
            getTickerData(stock.code)

            if count == numberOfStocks - 1:
                self.downloadingFinished.sig.emit()
                self.downloadingWindow.close()


class DownloadWindow(QProgressDialog):
    def __init__(self, parent=None):
        QProgressDialog.__init__(self, parent)
        self.setGeometry(300, 300, 300, 50)

    def setProgress(self, value):
        if value > 100:
            value = 100
        self.setValue(value)



