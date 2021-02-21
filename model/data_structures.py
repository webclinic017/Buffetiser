import enum
import json
import os


class InvestmentType(enum.Enum):
    Share = 1
    Crypto = 2


class Investment:
    def __init__(self, investmentType, conversion, code, name, costPerUnit, overallCost):
        self.investmentType = investmentType
        self.code = str(code)
        self.name = str(name)
        self.costPerUnit = float(costPerUnit) if costPerUnit else None
        self.overallCost = float(overallCost) if overallCost else None
        self.held = 0
        self.live = -1
        self.conversion = conversion
        self.priceHistory = {}
        self.getTickerData(code)

        self.setDefaultLivePrice()

    def setDefaultLivePrice(self):
        self.live = self.priceHistory['close'][-1] * self.conversion

    def livePrice(self):
        return self.live * self.conversion

    def totalCost(self):
        return self.overallCost if self.overallCost else (self.held * self.costPerUnit * self.conversion)

    def totalValue(self):
        return self.held * self.live * self.conversion

    def profit(self):
        return self.totalValue() - self.totalCost()

    def percentProfit(self):
        return ((self.totalValue() / self.totalCost()) - 1) * 100

    def getTickerData(self, code):
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
                    prices['high'].append(entry['high'] * self.conversion)
                    prices['low'].append(entry['low'] * self.conversion)
                    prices['close'].append(entry['close'] * self.conversion)

        self.priceHistory = prices


class Share(Investment):
    def __init__(self, investmentType, conversion, code, name, held, costPerUnit, overallCost):
        super().__init__(investmentType, conversion, code, name, costPerUnit, overallCost)
        self.held = int(held)


class Crypto(Investment):
    def __init__(self, investmentType, conversion, code, name, held, costPerUnit, overallCost):
        super().__init__(investmentType, conversion, code, name, costPerUnit, overallCost)
        self.held = float(held)