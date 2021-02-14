import csv

from model.data_structures import InvestmentType, Share, Crypto
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
                    self.portfolio.append(Share(InvestmentType.Share,
                                                row[1],
                                                row[2],
                                                row[3],
                                                row[4]))
                elif row[0] == 'crypto':
                    self.portfolio.append(Crypto(InvestmentType.Crypto,
                                                 row[1],
                                                 row[2],
                                                 row[3],
                                                 row[4]))

    def readAllLive(self, _):
        progressDialog = DownloadWindow()
        progressDialog.show()
        dlTread = DownloadThread(self.fatController, progressDialog)
        dlTread.downloadingFinished.sig.connect(self.fatController.view.updateLivePrice)
        dlTread.start()

    def calculatePortfolioTotals(self):

        # Calculate the total sum of all investments for each day for the 100 days
        portfolioSum = []
        for day in range(0, 255):
            daySum = 0
            for stock in self.portfolio:
                try:
                    daySum += stock.priceHistory['close'][day]
                except IndexError:
                    pass  # It doesn't matter
            portfolioSum.append(daySum)

        return portfolioSum




