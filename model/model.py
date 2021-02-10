import csv

from model.data_handlers import Stock, getTickerData
from view.download_window import DownloadWindow, DownloadThread


class Model:
    def __init__(self, fatController):

        self.fatController = fatController

        self.portfolio = []

    def portfolioSetup(self):

        with open('config.csv') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            for row in csvReader:
                if row[0] == 'key':
                    self.fatController.key = row[1]
                elif row[0] == 'share':
                    self.portfolio.append(Stock(row[1], row[2], row[3], row[4], getTickerData(row[1])))

    def readAllLive(self, _):
        progressDialog = DownloadWindow()
        progressDialog.show()
        dlTread = DownloadThread(self.fatController, progressDialog)
        dlTread.downloadingFinished.sig.connect(self.fatController.view.updateView())
        dlTread.start()

    def calculatePortfolioTotals(self):

        # Calculate the total sum of all shares for the last year
        portfolioSum = []
        for day in range(0, len(self.portfolio)):
            daySum = 0
            for stock in self.portfolio:
                daySum += stock.prices['close'][day] * stock.held
            portfolioSum.append(daySum)

        return portfolioSum





    def totalsStock(self, text):
        print('stocks {}'.format(text))



