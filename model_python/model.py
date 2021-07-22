from control.network_controller import getCurrentCurrencyConversionRate
from view.download_window import DownloadThread


class Model:
    def __init__(self, fatController):

        self.fatController = fatController
        self.portfolio = []
        getCurrentCurrencyConversionRate()

    def readAllLive(self, _):
        self.fatController.downloadThread = DownloadThread(self.fatController)
        self.fatController.downloadThread.downloadingFinished.sig.connect(self.fatController.view.updateAllFields)
        self.fatController.downloadThread.start()

    def calculatePortfolioTotals(self):
        """
        :return: Total sum of all investments for each day for the 100(ish) days.
        """
        portfolioSum = {}

        for investment in self.portfolio:
            for entry in investment.priceHistory:
                if entry['date'] in portfolioSum:
                    portfolioSum[entry['date']] += float(entry['close'])
                else:
                    portfolioSum[entry['date']] = float(entry['close'])

        # get rid of garbage at the end
        return list(portfolioSum.values())[0:-3]



