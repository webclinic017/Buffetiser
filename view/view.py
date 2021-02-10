import os
import tempfile

import pygal
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout

from view.config_dialog import ConfigDialog
from view.main_window import MainWindow


def plotPriceHistory(stock):
    stockPlot = pygal.Line(width=1000,
                           height=300,
                           show_dots=False,
                           show_y_guides=False,
                           max_scale=6,
                           legend_box_size=5,
                           x_label_rotation=6.25,
                           show_minor_x_labels=False)
    stockPlot.title = '{} ({})'.format(stock.name, stock.code)

    dateList = [x for x in stock.prices['date']]
    stockPlot.x_labels = dateList
    stockPlot.x_labels_major = dateList[::48]

    stockPlot.add('Low', stock.prices['low'])
    stockPlot.add('High', stock.prices['high'])
    stockPlot.add('Close', stock.prices['close'])
    plotWidget = QLabel()
    path = os.path.join(tempfile.gettempdir(), 'buffetiser.png')
    stockPlot.render_to_png(path)
    plotWidget.setPixmap(QPixmap(path))
    os.remove(path)

    return plotWidget


class View:
    def __init__(self, fatController):

        self.fatController = fatController
        self.portfolio = fatController.model.portfolio
        self.row = 0

        self.topLayout = QGridLayout()
        self.bottomLayout = QGridLayout()
        self.sideLayout = QVBoxLayout()

    def showMainWindow(self):

        window = MainWindow(self.fatController)
        window.show()

    def updateView(self):
        print('update view')

    def config(self, _):
        config = ConfigDialog(self.fatController)
        config.show()

    def createPanel(self, stock):

        detailsPanel = QWidget()
        detailsPanel.setFixedWidth(1200)
        detailsPanel.setStyleSheet("""QWidget{ background-color: white;} """)
        detailsLayout = QGridLayout()
        detailsLayout.setContentsMargins(0, 0, 0, 0)
        detailsLayout.setSpacing(0)
        detailsPanel.setLayout(detailsLayout)

        detailsLayout.addWidget(plotPriceHistory(stock), 0, 0, 5, 1)

        costPrice = stock.held * stock.cost
        currentPrice = float(stock.prices['close'][-1])
        currentValue = stock.held * currentPrice

        label = QLabel('Cost:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 0, 1)
        label = QLabel('${:.2f}'.format(costPrice))
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

        label = QLabel('Current Price:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 2, 1)
        label = QLabel('${:.2f}'.format(stock.currentPrice))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD; 
                        border-right: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 2, 2)

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
        detailsLayout.addWidget(label, 3, 1)
        label = QLabel('${:.2f}'.format(currentValue))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD; 
                        border-right: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 3, 2)

        label = QLabel('Profit:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 4, 1)
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
        detailsLayout.addWidget(label, 4, 2)

        label = QLabel('')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-left: 1px solid #DDD;} """)
        detailsLayout.addWidget(label, 5, 1)
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
        detailsLayout.addWidget(label, 5, 2)

        self.topLayout.addWidget(detailsPanel, self.row, 0)

        spacer = QLabel('')
        spacer.setFixedHeight(5)
        self.topLayout.addWidget(spacer, self.row + 1, 0)
        self.row += 2

    def plotPortfolioValueHistory(self):

        totalsPlot = pygal.Line(width=1000,
                                height=200,
                                y_labels_major_every=100,
                                show_dots=False,
                                show_y_guides=False,
                                max_scale=6,
                                legend_box_size=5)
        totalsPlot.title = "Total Portfolio Value"
        totalsPlot.add('Sum', self.fatController.model.calculatePortfolioTotals())
        path = os.path.join(tempfile.gettempdir(), 'buffetizer.png')
        totalsPlot.render_to_png(path)
        plotWidget = QLabel()
        plotWidget.setPixmap(QPixmap(path))
        os.remove(path)

        return plotWidget

    def createTotalsPanel(self):

        self.bottomLayout.addWidget(self.fatController.view.plotPortfolioValueHistory(), 0, 0, 4, 1)

        totalCost = 0
        totalValue = 0
        for stock in self.portfolio:
            totalCost += stock.held * stock.cost
            totalValue += stock.held * float(stock.prices['close'][-1])

        label = QLabel('Cost:')
        label.setFixedWidth(100)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; 
                        padding-right: 10px; 
                        border-left: 1px solid #DDD; 
                        border-bottom: 1px solid #DDD;} """)
        self.bottomLayout.addWidget(label, 0, 1)
        label = QLabel('${:.2f}'.format(totalCost))
        label.setFixedWidth(110)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 25px; 
                        border-left: 1px solid #DDD; 
                        border-right: 2px solid #FFF; 
                        border-bottom: 1px solid #DDD;} """)
        self.bottomLayout.addWidget(label, 0, 2)

        label = QLabel('Value:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        self.bottomLayout.addWidget(label, 1, 1)
        label = QLabel('${:.2f}'.format(totalValue))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 25px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        self.bottomLayout.addWidget(label, 1, 2)

        label = QLabel('Profit:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        self.bottomLayout.addWidget(label, 2, 1)
        label = QLabel('${:.2f}'.format(totalValue - totalCost))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 25px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        self.bottomLayout.addWidget(label, 2, 2)

        label = QLabel('')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 10px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        self.bottomLayout.addWidget(label, 3, 1)
        label = QLabel('{:.2f}%'.format(((totalValue - totalCost) / totalCost) * 100))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet(
            """QWidget{ padding-right: 25px; border-left: 1px solid #DDD; border-bottom: 1px solid #DDD;} """)
        self.bottomLayout.addWidget(label, 3, 2)


