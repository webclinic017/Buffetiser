import os
import tempfile

import pygal
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel

from model.data_structures import InvestmentType


class investmentPanel(QWidget):
    def __init__(self, investment):
        super(investmentPanel, self).__init__()

        self.investment = investment
        self.livePriceLabel = QLabel()
        self.createPanel(investment)

    def updateLivePrice(self, investment):
        if self.investment.code == self.investment.code:
            self.livePriceLabel.setText('${:.2f}'.format(investment.livePrice))

    def createPanel(self, investment):

        self.setFixedWidth(1200)
        self.setStyleSheet("""QWidget{ background-color: white;} """)
        detailsLayout = QGridLayout()
        detailsLayout.setContentsMargins(0, 0, 0, 0)
        detailsLayout.setSpacing(0)
        self.setLayout(detailsLayout)

        detailsLayout.addWidget(self.plotPriceHistory(), 0, 0, 7, 1)

        costPrice = investment.held * investment.cost
        currentPrice = float(investment.livePrice) if float(investment.livePrice) > 0 else float(investment.priceHistory['close'][-1])
        currentValue = investment.held * currentPrice

        label = QLabel('Cost Price:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 0, 1)
        label = QLabel('${:.2f}'.format(investment.cost))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-right: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 0, 2)

        label = QLabel('Held:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 1, 1)
        label = QLabel('{:.4f}'.format(investment.held))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD; 
                        border-right: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 1, 2)

        label = QLabel('Cost:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 2, 1)
        label = QLabel('${:.2f}'.format(costPrice))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-right: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 2, 2)

        label = QLabel('Live Price:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 3, 1)
        self.livePriceLabel.setText('${:.2f}'.format(investment.livePrice))
        self.livePriceLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.livePriceLabel.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD; 
                        border-right: 1px solid #DDD;} """)
        detailsLayout.addWidget(self.livePriceLabel, 3, 2)

        label = QLabel('Value:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        label = QLabel('Value:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 4, 1)
        label = QLabel('${:.2f}'.format(currentValue))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD; 
                        border-right: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 4, 2)

        label = QLabel('Profit:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 5, 1)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        profitLabel = QLabel()
        if investment.profit() > 0:
            profitLabel.setStyleSheet(
                """QWidget{ color: green; 
                            padding-right: 10px; 
                            border-left: 1px solid #DDD; 
                            border-bottom: 1px solid #DDD; 
                            border-right: 1px solid #DDD;} """)
            profitTextFormat = '${:.2f}'
        else:
            profitLabel.setStyleSheet(
                """QWidget{ color: red; 
                            padding-right: 10px; 
                            border-left: 1px solid #DDD; 
                            border-bottom: 1px solid #DDD; 
                            border-right: 1px solid #DDD;} """)
            profitTextFormat = '-${:.2f}'
        profitLabel.setText(profitTextFormat.format(abs(investment.profit())))
        profitLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        detailsLayout.addWidget(profitLabel, 5, 2)

        label = QLabel('')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-left: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 6, 1)
        percentProfit = ((currentPrice - investment.cost) / investment.cost) * 100
        label = QLabel('{:.2f}%'.format(percentProfit))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if percentProfit > 0:
            label.setStyleSheet(
                """QWidget{ color: green; 
                            padding-right: 10px; 
                            border-left: 1px solid #DDD; 
                            border-right: 1px solid #DDD;} """)
        else:
            label.setStyleSheet(
                """QWidget{ color: red; 
                            padding-right: 10px; 
                            border-left: 1px solid #DDD; 
                            border-right: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 6, 2)

    def plotPriceHistory(self):
        investmentPlot = pygal.Line(width=1000,
                                    height=300,
                                    show_dots=False,
                                    show_y_guides=False,
                                    max_scale=6,
                                    legend_box_size=5,
                                    x_label_rotation=6.25,
                                    show_minor_x_labels=False)
        investmentPlot.title = '{} ({})'.format(self.investment.name, self.investment.code)

        dateList = [x for x in self.investment.priceHistory['date']]
        investmentPlot.x_labels = dateList
        investmentPlot.x_labels_major = dateList[::48]
        investmentPlot.add('Low', self.investment.priceHistory['low'])
        investmentPlot.add('High', self.investment.priceHistory['high'])
        investmentPlot.add('Close', self.investment.priceHistory['close'])
        plotWidget = QLabel()
        path = os.path.join(tempfile.gettempdir(), 'buffetiser.png')
        investmentPlot.render_to_png(path)
        plotWidget.setPixmap(QPixmap(path))
        os.remove(path)

        return plotWidget
