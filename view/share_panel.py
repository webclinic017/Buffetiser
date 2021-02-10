import os
import tempfile

import pygal
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel


class SharePanel(QWidget):
    def __init__(self, stock):
        super(SharePanel, self).__init__()

        self.stock = stock
        self.livePriceLabel = QLabel()
        self.createPanel(stock)

    def updateLivePrice(self, price):
        print('update {} to {}'.format(self.stock.code, price))
        self.livePriceLabel.setText('${:.2f}'.format(price))

    def createPanel(self, stock):

        self.setFixedWidth(1200)
        self.setStyleSheet("""QWidget{ background-color: white;} """)
        detailsLayout = QGridLayout()
        detailsLayout.setContentsMargins(0, 0, 0, 0)
        detailsLayout.setSpacing(0)
        self.setLayout(detailsLayout)

        detailsLayout.addWidget(self.plotPriceHistory(), 0, 0, 7, 1)

        costPrice = stock.held * stock.cost
        currentPrice = float(stock.prices['close'][-1])
        currentValue = stock.held * currentPrice

        label = QLabel('Cost Price:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 0, 1)
        label = QLabel('${:.2f}'.format(stock.cost))
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
        label = QLabel('{}'.format(stock.held))
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
        self.livePriceLabel.setText('${:.2f}'.format(stock.livePrice))
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
        profit = currentValue - costPrice
        label = QLabel('${:.2f}'.format(profit))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if profit > 0:
            label.setStyleSheet(
                """QWidget{ color: green; 
                            padding-right: 10px; 
                            border-left: 1px solid #DDD; 
                            border-bottom: 1px solid #DDD; 
                            border-right: 1px solid #DDD;} """)
        else:
            label.setStyleSheet(
                """QWidget{ color: red; 
                            padding-right: 10px; 
                            border-left: 1px solid #DDD; 
                            border-bottom: 1px solid #DDD; 
                            border-right: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 5, 2)

        label = QLabel('')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-left: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 6, 1)
        percentProfit = ((currentPrice - stock.cost) / stock.cost) * 100
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
        stockPlot = pygal.Line(width=1000,
                               height=300,
                               show_dots=False,
                               show_y_guides=False,
                               max_scale=6,
                               legend_box_size=5,
                               x_label_rotation=6.25,
                               show_minor_x_labels=False)
        stockPlot.title = '{} ({})'.format(self.stock.name, self.stock.code)

        dateList = [x for x in self.stock.prices['date']]
        stockPlot.x_labels = dateList
        stockPlot.x_labels_major = dateList[::48]

        stockPlot.add('Low', self.stock.prices['low'])
        stockPlot.add('High', self.stock.prices['high'])
        stockPlot.add('Close', self.stock.prices['close'])
        plotWidget = QLabel()
        path = os.path.join(tempfile.gettempdir(), 'buffetiser.png')
        stockPlot.render_to_png(path)
        plotWidget.setPixmap(QPixmap(path))
        os.remove(path)

        return plotWidget
