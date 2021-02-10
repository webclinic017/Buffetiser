import os
import tempfile

import pygal
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGridLayout, QLabel, QVBoxLayout

from view.config_dialog import ConfigDialog
from view.main_window import MainWindow
from view.share_panel import SharePanel





class View:
    def __init__(self, fatController):

        self.fatController = fatController
        self.portfolio = fatController.model.portfolio
        self.row = 0
        self.mainWindow = None
        self.allSharePanels = {}

        self.topLayout = QGridLayout()
        self.bottomLayout = QGridLayout()
        self.sideLayout = QVBoxLayout()

    def showMainWindow(self):

        self.mainWindow = MainWindow(self.fatController)
        self.mainWindow.show()

    def updateView(self):
        print('update SharePanels')
        for share in self.portfolio:
            self.allSharePanels[share.code].updateLivePrice(share.livePrice)

    def config(self, _):
        config = ConfigDialog(self.fatController)
        config.show()

    def createPanel(self, stock):

        panel = SharePanel(stock)
        self.allSharePanels[stock.code] = panel
        self.topLayout.addWidget(panel, self.row, 0)

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


