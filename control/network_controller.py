import json
import os
from json import JSONDecodeError

import requests
from bs4 import BeautifulSoup

from control.config import DATA_PATH
from control.file_io_controller import writeInvestmentDataFile, writeCurrencyConversionValue
from model.CoinSpot import Coinspot


def getCurrentCurrencyConversionRate():
    url = 'https://v6.exchangerate-api.com/v6/' + \
          'da52a4f4e127f7d7c51b87ab' + \
          '/latest/USD'
    response = requests.get(url=url).json()
    currencyConversion = float(response['conversion_rates']['AUD'])
    writeCurrencyConversionValue(currencyConversion)

    return currencyConversion


def useBigCharts(today, investment):
    """
    Uses ASX data from BigCharts (MarketWatch) to propagate portfolio with share data.
    There is no official API so data is scraped fro website. Not sure if this breaks terms of use.
    :param today: The date when call is made.
    :param investment: The Investment object to fetch data for.
    """
    shareHistory = investment.priceHistory
    todayString = '{}-{}-{}'.format(today.year, today.month, today.strftime("%d"))

    url = 'https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb=' + \
          'au:{}+'.format(investment.code)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for entry in soup.findAll('td', {'class': 'symb-col'}):
        symbol = entry.text
        lastPrice = soup.find('td', {'class': 'last-col'}).text
        high = soup.find('td', {'class': 'high-col'}).text
        low = soup.find('td', {'class': 'low-col'}).text
        volume = soup.find('td', {'class': 'volume-col'}).text
        investment.currentPrice = float(lastPrice)

        currentPriceObject = {"date": todayString,
                              "open": float(low),
                              "high": float(high),
                              "low": float(low),
                              "close": float(lastPrice),
                              "adjusted_close": float(lastPrice),
                              "volume": int(volume.replace(',', ''))}

        # Don't want to add multiple entries for the same day.
        if todayString in [entry['date'] for entry in shareHistory]:
            return
        else:
            shareHistory.append(currentPriceObject)

            writeInvestmentDataFile(investment.code, shareHistory)


"""----------------------- Yet to be implemented/used -----------------------"""


def scrapeAsx(self, today, investment):
    cookies = dict(cookie='5f7ce238-f616-4f14-b9c0-f8c68908e5fa#uid#dodgydesigns@gmail.com')

    url = 'https://www2.asx.com.au/content/asx/investor/dashboard.html'
    url = 'https://www2.asx.com.au/'
    # url = 'https://myasx.asx.com.au/home/login.do'
    # url = 'https://www2.asx.com.au/new#login'
    res = requests.get(url, cookies=cookies, auth=HTTPDigestAuth('dodgydesigns@gmail.com', '!!Apple01!!'))
    # cookies=cookies,
    print(res.text)
    print(res.status_code)


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
              '{}-{}-{}'.format(today.year, today.month - 1, today.strftime("%d")) + \
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

