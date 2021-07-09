import os
import tempfile

import pygal
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel

from control.config import COLOUR0, COLOUR3, RED, GREEN, INVESTMENT_PLOT_STYLE
from model.data_structures import Crypto


class investmentPanel(QWidget):
    def __init__(self, investment):
        super(investmentPanel, self).__init__()

        self.investment = investment
        self.livePriceLabel = QLabel()
        self.currentValueLabel = QLabel()
        self.profitLabel = QLabel()
        self.percentProfitLabel = QLabel()
        self.priceHistoryPlot = QLabel()

        self.detailsLayout = QGridLayout()

        self.createPanel(investment)

    def createPanel(self, investment):

        self.setStyleSheet("""QWidget{ background-color: """ + COLOUR0 + """; color: """ + COLOUR3 + """} """)
        self.detailsLayout.setContentsMargins(0, 0, 0, 0)
        self.detailsLayout.setSpacing(0)
        self.setLayout(self.detailsLayout)

        label = QLabel('Cost Price:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-top: 1px solid """ + COLOUR3 + """; 
                                        border-left: 1px solid  """ + COLOUR3 + """; 
                                        border-bottom: 1px solid  """ + COLOUR3 + """;} """)
        self.detailsLayout.addWidget(label, 0, 1)
        label = QLabel('${:.2f}'.format(investment.costPerUnit))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-top: 1px solid """ + COLOUR3 + """; 
                        border-left: 1px solid """ + COLOUR3 + """; 
                        border-right: 1px solid """ + COLOUR3 + """; 
                        border-bottom: 1px solid """ + COLOUR3 + """;} """)
        self.detailsLayout.addWidget(label, 0, 2)

        label = QLabel('Held:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid  """ + COLOUR3 + """; 
                        border-bottom: 1px solid  """ + COLOUR3 + """} """)
        self.detailsLayout.addWidget(label, 1, 1)
        heldText = '{:.4f}'.format(investment.held) if investment.investmentType == Crypto \
            else '{}'.format(investment.held)
        label = QLabel(heldText)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid  """ + COLOUR3 + """; 
                        border-bottom: 1px solid  """ + COLOUR3 + """; 
                        border-right: 1px solid  """ + COLOUR3 + """;} """)
        self.detailsLayout.addWidget(label, 1, 2)

        label = QLabel('Total Cost:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet( """QWidget{ padding-right: 10px; 
                                         border-left: 1px solid  """ + COLOUR3 + """; 
                                         border-bottom: 1px solid  """ + COLOUR3 + """;} """)
        self.detailsLayout.addWidget(label, 2, 1)
        label = QLabel('${:.2f}'.format(self.investment.totalCost()))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid  """ + COLOUR3 + """; 
                        border-right: 1px solid  """ + COLOUR3 + """; 
                        border-bottom: 1px solid  """ + COLOUR3 + """;} """)
        self.detailsLayout.addWidget(label, 2, 2)

        label = QLabel('Live Price:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid  """ + COLOUR3 + """; 
                        border-bottom: 1px solid  """ + COLOUR3 + """;} """)

        self.detailsLayout.addWidget(label, 3, 1)
        label = QLabel('Value:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid  """ + COLOUR3 + """; 
                        border-bottom: 1px solid  """ + COLOUR3 + """;} """)
        self.detailsLayout.addWidget(label, 4, 1)

        label = QLabel('Profit:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid  """ + COLOUR3 + """; 
                        border-bottom: 1px solid  """ + COLOUR3 + """;} """)
        self.detailsLayout.addWidget(label, 5, 1)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label = QLabel('')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-left: 1px solid  """ + COLOUR3 + """;
                                        border-bottom: 1px solid  """ + COLOUR3 + """;} """)
        self.detailsLayout.addWidget(label, 6, 1)

        self.livePriceLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.currentValueLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.profitLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.percentProfitLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.detailsLayout.addWidget(self.priceHistoryPlot, 0, 0, 7, 1)
        self.detailsLayout.addWidget(self.livePriceLabel, 3, 2)
        self.detailsLayout.addWidget(self.currentValueLabel, 4, 2)
        self.detailsLayout.addWidget(self.profitLabel, 5, 2)
        self.detailsLayout.addWidget(self.percentProfitLabel, 6, 2)

        self.updatePriceHistoryPlot()
        self.livePrice()
        self.currentValue()
        self.profit()
        self.percentProfit()

    def updateAll(self):
        self.updatePriceHistoryPlot()
        self.livePrice()
        self.currentValue()
        self.profit()
        self.percentProfit()

    def plotPriceHistory(self):

        self.investment.getTickerData(self.investment.code)

        investmentPlot = pygal.Line(width=1000,
                                    height=300,
                                    show_dots=False,
                                    show_y_guides=False,
                                    max_scale=6,
                                    legend_box_size=5,
                                    x_label_rotation=6.25,
                                    show_minor_x_labels=False,
                                    style=INVESTMENT_PLOT_STYLE)
        investmentPlot.title = '{} ({})'.format(self.investment.name, self.investment.code)

        dateList = [x for x in self.investment.priceHistory['date']]
        investmentPlot.x_labels = dateList
        investmentPlot.x_labels_major = dateList[::48]
        investmentPlot.add('Low', self.investment.priceHistory['low'])
        investmentPlot.add('High', self.investment.priceHistory['high'])
        investmentPlot.add('Close', self.investment.priceHistory['close'])
        path = os.path.join(tempfile.gettempdir(), 'buffetiser.png')
        investmentPlot.render_to_png(path)

        return path

    def livePrice(self):
        self.livePriceLabel.setText('${:.2f}'.format(self.investment.livePrice()))
        self.livePriceLabel.setStyleSheet("""QLabel{ padding-right: 10px;
                                                     border-left: 1px solid  """ + COLOUR3 + """;
                                                     border-bottom: 1px solid  """ + COLOUR3 + """;
                                                     border-right: 1px solid  """ + COLOUR3 + """;} """)

    def currentValue(self):
        self.currentValueLabel.setText('${:.2f}'.format(self.investment.totalValue()))
        self.currentValueLabel.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid  """ + COLOUR3 + """; 
                        border-bottom: 1px solid  """ + COLOUR3 + """; 
                        border-right: 1px solid  """ + COLOUR3 + """;} """)

    def profit(self):
        if self.investment.profit() > 0:
            self.profitLabel.setStyleSheet(
                """QWidget{ color: """ + GREEN + """; 
                            padding-right: 10px; 
                            border-left: 1px solid  """ + COLOUR3 + """; 
                            border-bottom: 1px solid  """ + COLOUR3 + """; 
                            border-right: 1px solid  """ + COLOUR3 + """;} """)
            profitTextFormat = '${:.2f}'
        else:
            self.profitLabel.setStyleSheet(
                """QWidget{ color: """ + RED + """; 
                            padding-right: 10px; 
                            border-left: 1px solid  """ + COLOUR3 + """; 
                            border-bottom: 1px solid  """ + COLOUR3 + """; 
                            border-right: 1px solid  """ + COLOUR3 + """;} """)
            profitTextFormat = '-${:.2f}'
        self.profitLabel.setText(profitTextFormat.format(abs(self.investment.profit())))

    def percentProfit(self):
        self.percentProfitLabel.setText('{:.2f}%'.format(self.investment.percentProfit()))
        if self.investment.percentProfit() > 0:
            self.percentProfitLabel.setStyleSheet(
                """QWidget{ color: """ + GREEN + """; 
                            padding-right: 10px; 
                            border-left: 1px solid  """ + COLOUR3 + """; 
                            border-right: 1px solid  """ + COLOUR3 + """;
                            border-bottom: 1px solid  """ + COLOUR3 + """;} """)
        else:
            self.percentProfitLabel.setStyleSheet(
                """QWidget{ color: """ + RED + """; 
                            padding-right: 10px; 
                            border-left: 1px solid  """ + COLOUR3 + """; 
                            border-right: 1px solid  """ + COLOUR3 + """;
                            border-bottom: 1px solid  """ + COLOUR3 + """;} """)

    def updatePriceHistoryPlot(self):
        path = self.plotPriceHistory()
        self.priceHistoryPlot.setPixmap(QPixmap(path))
        os.remove(path)
