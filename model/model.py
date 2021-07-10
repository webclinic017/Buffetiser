import csv
import os
import requests

from control.file_io_controller import validateConfigFile
from control.network_controller import getCurrentCurrencyConversionRate
from model.data_structures import InvestmentType, Share, Crypto
from view.download_window import DownloadThread
from control.config import DATA_PATH


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
        portfolioSum = []
        for day in range(0, 255):
            daySum = 0
            for investment in self.portfolio:
                try:
                    daySum += float(investment.priceHistory[day]['close']) * investment.conversion
                except IndexError:
                    pass  # It doesn't matter
            portfolioSum.append(daySum)

        return portfolioSum


