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
                print('Unexpected FileExistsError while creating data directory:',error)
        except OSError as error:
            print('Unexpected OSError while creating data directory:',error)

        numberOfStocks = len(self.portfolio)
        for count, investment in enumerate(self.portfolio):
            # Update historical share data
            if investment.investmentType == InvestmentType.Share:
                pass
                url = 'https://eodhistoricaldata.com/api/eod/' + \
                      investment.code + \
                      '.AU?api_token=' + \
                      self.fatController.key + \
                      '&fmt=json' + \
                      '&from=' + str(today.year-1) + '-' + str(today.month) + '-' + today.strftime("%d") + \
                      '&to=' + str(today.year) + '-' + str(today.month) + '-' + today.strftime("%d") + \
                      '&g=m'
                response = requests.get(url=url).json()
                with open(os.path.join(DATA_PATH,f'data-{investment.code}.txt'), 'w') as outfile:
                    json.dump(response, outfile)

                # Update current priceHistory
                url = 'https://eodhistoricaldata.com/api/real-time/' + \
                      investment.code + \
                      '.AU?api_token=' + \
                      self.fatController.key + \
                      '&fmt=json'
                response = requests.get(url=url).json()
                investment.livePrice = response['close']
                self.downloadingWindow.setProgress(((1 + count) / numberOfStocks) * 100)
                self.downloadingWindow.setLabelText(investment.code)
                self.downloadingFinished.sig.emit(investment)

            elif investment.investmentType == InvestmentType.Crypto:
                # Update historical crypto data
                url = 'https://eodhistoricaldata.com/api/eod/' + \
                      investment.code + \
                      '-USD.CC?api_token=' + \
                      self.fatController.key + \
                      '&order=m' + \
                      '&fmt=json'
                response = requests.get(url=url).json()
                with open(os.path.join(DATA_PATH,f'data-{investment.code}.txt'), 'w') as outfile:
                    json.dump(response, outfile)

                # Update current priceHistory
                url = 'https://eodhistoricaldata.com/api/real-time/' + \
                      investment.code + \
                      '-USD.CC?api_token=' + \
                      self.fatController.key + \
                      '&fmt=json'
                response = requests.get(url=url).json()
                price = response['close']
                if price == 'NA':
                    price = investment.priceHistory['close'][-1]

                conversion = float(
                    requests.get(url='https://www.freeforexapi.com/api/live?pairs=USDAUD').json()['rates']['USDAUD'][
                        'rate'])
                investment.livePrice = float(price) * float(conversion)  # in AUD


class DownloadWindow(QProgressDialog):
    def __init__(self, parent=None):
        QProgressDialog.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setGeometry(300, 300, 300, 50)

    def setProgress(self, value):
        if value >= 100:
            value = 100
        self.setValue(value)
