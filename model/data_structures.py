import enum


class Config:
    def __init__(self):
        self.dataSupplier = '-'
        self.dataAccessKey = '-'
        self.exchange = '-'
        self.currency = '-'
        self.currencyConversionKey = '-'
        self.currencyConversion = '-'


class InvestmentType(enum.Enum):
    Share = 1
    Crypto = 2


class Investment:
    def __init__(self, investmentType, conversion, code, name, costPerUnit, overallCost, held):
        self.investmentType = investmentType
        self.conversion = float(conversion)
        self.code = str(code)
        self.name = str(name)
        self.costPerUnit = float(costPerUnit) if costPerUnit else None
        self.overallCost = float(overallCost) if overallCost else None
        self.held = int(held)
        self.currentPrice = -1
        self.priceHistory = None

    def setDefaultLivePrice(self):
        if self.priceHistory:
            self.currentPrice = float(self.priceHistory[-1]['close']) * self.conversion

    def livePrice(self):
        return self.currentPrice * self.conversion

    def totalCost(self):
        return self.overallCost if self.overallCost else (self.held * self.costPerUnit)

    def totalValue(self):
        return self.held * self.currentPrice * self.conversion

    def profit(self):
        return self.totalValue() - self.totalCost()

    def percentProfit(self):
        return ((self.totalValue() / self.totalCost()) - 1) * 100


class Share(Investment):
    def __init__(self, investmentType, conversion, code, name, held, costPerUnit, overallCost):
        super().__init__(investmentType, conversion, code, name, costPerUnit, overallCost, held)
        self.held = int(held)


class Crypto(Investment):
    def __init__(self, investmentType, conversion, code, name, held, costPerUnit, overallCost):
        super().__init__(investmentType, conversion, code, name, costPerUnit, overallCost)
        self.held = float(held)

    def livePrice(self):
        return 10.0
