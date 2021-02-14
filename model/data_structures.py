import enum
import json
import os


class InvestmentType(enum.Enum):
    Share = 1
    Crypto = 2


class Investment:
    def __init__(self, investmentType, code, name, cost):
        self.investmentType = investmentType
        self.code = str(code)
        self.name = str(name)
        self.cost = float(cost)
        self.held = 0
        self.priceHistory = {}
        self.getTickerData(code)
        self.livePrice = -1

        self.setDefaultLivePrice()

    def setDefaultLivePrice(self):
        self.livePrice = self.priceHistory['close'][-1]

    def totalCost(self):
        return self.held * self.cost

    def totalValue(self):
        return self.held * self.livePrice

    def profit(self):
        return self.totalValue() - self.totalCost()

    def percentProfit(self):
        return self.totalValue() / self.totalCost()

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
                    prices['high'].append(entry['high'])
                    prices['low'].append(entry['low'])
                    prices['close'].append(entry['close'])

        self.priceHistory = prices


class Share(Investment):
    def __init__(self, investmentType, code, name, held, cost):
        super().__init__(investmentType, code, name, cost)
        self.held = int(held)


class Crypto(Investment):
    def __init__(self, investmentType, code, name, held, cost):
        super().__init__(investmentType, code, name, cost)
        self.held = float(held)

    def totalCost(self):
        return self.held * self.cost

    def totalValue(self):
        return self.held * self.livePrice

    def percentProfit(self):
        return self.totalValue() / self.totalCost()



