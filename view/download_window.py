import json
import threading
import os
from datetime import datetime
from json.decoder import JSONDecodeError
# import websocket

import requests
from PySide2.QtCore import QObject, Signal, Qt
from PySide2.QtGui import QPalette, QBrush, QColor

from control.config import COLOUR0, COLOUR3, DATA_PATH
from model.CoinSpot import Coinspot
from model.data_structures import InvestmentType
from view.qroundprogressbar import QRoundProgressBar


class DownloadSignal(QObject):
    sig = Signal(object)


class DownloadThread(threading.Thread):
    downloadingFinished = DownloadSignal()

    def __init__(self, fatController, symbol=None):
        threading.Thread.__init__(self)
        self.downloadingWindow = fatController.view.mainWindow.progressDialog
        self.downloadingWindow.show()
        self.fatController = fatController
        self.portfolio = fatController.model.portfolio
        self.symbol = symbol
        self.halt = False

    def run(self):

        today = datetime.today()
        if self.symbol:
            self.portfolio = [stock.code for stock in self.portfolio if stock.code == self.symbol]

        numberOfStocks = len(self.portfolio)
        for count, investment in enumerate(self.portfolio):
            if not self.halt:
                if investment.investmentType == InvestmentType.Share:
                    # Update historical share data
                    self.getShare(today, investment)

                elif investment.investmentType == InvestmentType.Crypto:
                    # Update historical crypto data
                    self.getCrypto(today, investment)

                self.downloadingWindow.setProgress(((1 + count) / numberOfStocks) * 100, investment.code)
                self.downloadingFinished.sig.emit(investment)
        self.downloadingWindow.hide()

    def getShare(self, today, investment):
        """
        * FinnHub is > $50/month
        * Barchart is on-demand priced
        * EOD Historical Data $19/month
        * AlphaVantage $50/month   U45IF5IZFLOFNP82
        * IEX Cloud API no ASX
        * Intrinio consultation
        * Quandl no ASX
        * Polygon no ASX
        * Alpaca no ASX
        * Tradier no ASX
        * TwelveData $29/month
        :param today:
        :param investment:
        :return:
        """
        if self.fatController.dataSupplier == 'EOD':
            self.useEodHistoricData(today, investment)
        elif self.fatController.dataSupplier == 'tiingo':
            self.useTiingo(today, investment)
        elif self.fatController.dataSupplier == 'MarketStack':
            self.useMarketStack(today, investment)
        elif self.fatController.dataSupplier == 'xignite':
            self.useXignite(today, investment)
        elif self.fatController.dataSupplier == 'AlphaVantage':
            self.useAlphaVantage(today, investment)

    def useAlphaVantage(self, today, investment):
        # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=U45IF5IZFLOFNP82'
        url = 'https://au.finance.yahoo.com/quote/CBA.AX'
        response = requests.get(url=url).json()

        print('useAlphaVantage', response)

    def useXignite(self, today, investment):
        # header = xsd.Element(
        #     '{http://www.xignite.com/services/}Header',
        #     xsd.ComplexType([
        #         xsd.Element(
        #             '{http://www.xignite.com/services/}Username',
        #             xsd.String()
        #         )
        #     ])
        # )
        #
        # header_value = header(Username='6GPq4V5EyOPnMSUtTZMNVmUQIUjA')
        #
        # parameters = {
        #     'StartSymbol': 'AA',
        #     'EndSymbol': 'AAF'
        # }
        #
        # client = Client('http://navs.xignite.com/v2/xNAVs.asmx?WSDL')
        # result = client.service.ListSymbols(**parameters, _soapheaders=[header_value])

        # A real application should include some error handling. This example just prints the response.
        # print('-------------------', result)
        pass

    def useMarketStack(self, today, investment):
        """US Only"""
        try:
            # http:// api.marketstack.com / v1 / eod?access_key = 99
            #  & symbols = MP1.xasx & limit = 1
            url = 'http://api.marketstack.com/v1/' + \
                  'eod/latest?' + \
                  'access_key=' + \
                  self.fatController.key + \
                  '&symbols=' + \
                  investment.code + \
                  '.' + \
                  self.fatController.exchange + \
                  '&date_from=' + \
                  '2021-6-29' + \
                  '&date_to=' + \
                  '{}-{}-{}'.format(today.year, today.month-1, today.strftime("%d")) + \
                  '&date_to=' + \
                  '{}-{}-{}'.format(today.year, today.month, today.strftime("%d")) + \
                  '&limit=100'

            response = requests.get(url=url).json()

            with open(os.path.join(DATA_PATH, f'data-{investment.code}.txt'), 'w') as outfile:
                json.dump(response, outfile)

        except JSONDecodeError as e:
            self.fatController.showDialog("There was a problem getting data.\n"
                                          "Is your MarketStack API key valid?\n"
                                          "Error: " + str(e))
            return

    # noinspection PyMethodMayBeStatic
    def useTiingo(self, today, investment):
        """US Only"""
        pass
        # ws = websocket.create_connection("wss://api.tiingo.com/test")
        #
        # subscribe = {
        #     'eventName': 'subscribe',
        #     'eventData': {
        #         'authToken': 'a9ff0068d4215177bb02ba8b54eb894ae4ce45f7'
        #     }
        # }
        #
        # ws.send(json.dumps(subscribe))
        # while True:
        #     print(ws.recv(), today, investment)
        #     return ws.recv()

    def useEodHistoricData(self, today, investment):

        try:
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
            investment.currentPrice = float(response['close'])
        except JSONDecodeError as e:
            self.fatController.showDialog("There was a problem getting the currency conversion.\n"
                                          "Is your EOD Historical Data API key valid?\n"
                                          "Error: " + str(e))
            return

    def getCrypto(self, today, investment):

        # Get current currency conversion value
        url = 'https://eodhistoricaldata.com/api/real-time/' + \
              self.fatController.currency + \
              '.FOREX?api_token=' + \
              self.fatController.key + \
              '&fmt=json'
        try:
            self.fatController.currencyConversion = float(requests.get(url=url).json()['close'])
            self.fatController.model.writeCurrencyConversionValue()
        except JSONDecodeError as e:
            self.fatController.showDialog("There was a problem getting the currency conversion.\n"
                                          "Is your EOD Historical Data API key valid?\n"
                                          "Error: " + str(e))
            self.fatController.currencyConversion = 1

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
        with open(os.path.join(self.fatController.model.DATA_PATH, f'data-{investment.code}.txt'), 'w') as outfile:
            json.dump(response, outfile)

        # Update current priceHistory
        url = 'https://eodhistoricaldata.com/api/real-time/' + \
              investment.code + \
              '-USD.CC?api_token=' + \
              self.fatController.key + \
              '&fmt=json'
        response = requests.get(url=url).json()
        investment.conversion = self.fatController.currencyConversion
        investment.currentPrice = float(response['close']) * investment.conversion if response['close'] != 'NA' \
            else investment.priceHistory['close'][-1]

    def getCoinSpot(self):
        api_key = 'key'
        api_secret = 'secret'

        client = Coinspot(api_key, api_secret)
        print(client.balances())
        print(self.portfolio)


class DownloadWindow(QRoundProgressBar):
    def __init__(self):
        super(DownloadWindow, self).__init__()

        self.setBarStyle(QRoundProgressBar.BarStyle.DONUT)
        self.setStyleSheet("""QWidget {background-color: """ + COLOUR0 + """}""")
        palette = QPalette()
        brush = QBrush(QColor(COLOUR3))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)

        self.setPalette(palette)
        self.setFixedSize(50, 50)

    def setProgress(self, value, text):
        self.setValue(value, text)
