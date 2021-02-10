import csv
import json
import os


class Stock:
    def __init__(self, code, name, held, cost, prices):
        self.code = str(code)
        self.name = str(name)
        self.held = int(held)
        self.cost = float(cost)
        self.prices = prices
        self.currentPrice = -1


def getTickerData(code):

    prices = {'date': [],
              'high': [],
              'low': [],
              'close': []}

    if not os.path.isfile('data/data-{}.txt'.format(code)):
        for x in range(0, 100):
            prices['date'].append('-')
            prices['high'].append(x)
            prices['low'].append(x)
            prices['close'].append(x)
    else:
        with open('data/data-{}.txt'.format(code)) as json_file:
            response = json.load(json_file)

        for entry in response:
            if entry['date'] is None or \
                    entry['high'] is None or \
                    entry['low'] is None or \
                    entry['close'] is None:
                continue
            else:
                prices['date'].append(entry['date'])
                prices['high'].append(entry['high'])
                prices['low'].append(entry['low'])
                prices['close'].append(entry['close'])

    return prices


def getCurrentPrice(stock):
    pass


def updatePortfolio():
    pass






