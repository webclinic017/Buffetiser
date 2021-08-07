import threading
from datetime import datetime

from PySide2.QtCore import QObject, Signal, Qt
from PySide2.QtGui import QPalette, QBrush, QColor

from control.config import COLOUR0, COLOUR3
from control.network_controller import useBigCharts
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
        dataSupplier = self.fatController.config.dataSupplier
        if dataSupplier == 'EOD':
            self.useEodHistoricData(today, investment)
        elif dataSupplier == 'tiingo':
            self.useTiingo(today, investment)
        elif dataSupplier == 'MarketStack':
            self.useMarketStack(today, investment)
        elif dataSupplier == 'xignite':
            self.useXignite(today, investment)
        elif dataSupplier == 'AlphaVantage':
            self.useAlphaVantage(today, investment)
        elif dataSupplier == 'BigCharts':
            useBigCharts(today, investment)
            self.fatController.view.updateTotalsPanel()
        elif dataSupplier == 'scrape':
            self.scrapeAsx(today, investment)


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
