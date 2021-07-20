import os
import tempfile

import pygal
from PySide2 import QtWebEngineWidgets
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QPixmap, QDesktopServices
from PySide2.QtWidgets import QGridLayout, QLabel, QVBoxLayout

from control.config import COLOUR3, RED, GREEN, TOTALS_PLOT_STYLE
from view.config_dialog import ConfigDialog
from view.main_window import MainWindow
from view.investment_panel import InvestmentPanel


class View:
    def __init__(self, fatController):

        self.fatController = fatController
        self.row = 0
        self.mainWindow = None
        self.allInvestmentPanels = {}

        self.priceHistoryPlot = QtWebEngineWidgets.QWebEngineView()

        self.profitLabel = QLabel()
        self.percentProfitLabel = QLabel()

        self.topLayout = QGridLayout()
        self.bottomLayout = QGridLayout()
        self.sideLayout = QVBoxLayout()

    def showMainWindow(self):

        self.mainWindow = MainWindow(self.fatController)
        self.mainWindow.show()

    def updateAllFields(self, investment):
        self.allInvestmentPanels[investment.code].updateAll()

    def help(self, _):
        QDesktopServices.openUrl(QUrl('file:help/index.html'))

    def config(self, _):
        config = ConfigDialog(self.fatController)
        config.show()

    def createPanel(self, investment):

        panel = InvestmentPanel(investment)
        self.allInvestmentPanels[investment.code] = panel
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
                                legend_box_size=5,
                                style=TOTALS_PLOT_STYLE)
        totalsPlot.title = "Total Portfolio Value"
        totalsPlot.add('Sum', self.fatController.model.calculatePortfolioTotals())
        path = os.path.join(tempfile.gettempdir(), 'buffetizer-totals.svg')
        totalsPlot.render_to_file(path)

        return path

    def updateTotalsPanel(self):
        pass

    def createTotalsPanel(self):

        path = self.plotPortfolioValueHistory()
        self.priceHistoryPlot.load(QUrl.fromLocalFile(path))
        self.bottomLayout.addWidget(self.priceHistoryPlot, 0, 0, 4, 1)

        totalCost = 0
        totalValue = 0
        totalPercentProfit = 0

        for investment in self.fatController.model.portfolio:
            totalCost += investment.totalCost()
            totalValue += investment.totalValue()

        if len(self.fatController.model.portfolio) > 0:
            totalPercentProfit = ((totalValue / totalCost) - 1) * 100

        label = QLabel('Cost:')
        label.setFixedWidth(100)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-left: 1px solid """ + COLOUR3 + """;
                                        border-top: 1px solid """ + COLOUR3 + """;
                                        border-bottom: 1px solid """ + COLOUR3 + """;
                                        ;} """)

        self.bottomLayout.addWidget(label, 0, 1)
        label = QLabel('${:.2f}'.format(totalCost))
        label.setFixedWidth(110)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border: 1px solid """ + COLOUR3 + """;
                                        margin-right: 1px} """)
        self.bottomLayout.addWidget(label, 0, 2)

        label = QLabel('Value:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-left: 1px solid """ + COLOUR3 + """; 
                                        border-bottom: 1px solid """ + COLOUR3 + """;}""")
        self.bottomLayout.addWidget(label, 1, 1)
        label = QLabel('${:.2f}'.format(totalValue))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-left: 1px solid """ + COLOUR3 + """;
                                        border-right: 1px solid """ + COLOUR3 + """;
                                        border-bottom: 1px solid """ + COLOUR3 + """;
                                        margin-right: 1px} """)
        self.bottomLayout.addWidget(label, 1, 2)

        label = QLabel('Profit:')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-left: 1px solid """ + COLOUR3 + """; 
                                        border-bottom: 1px solid """ + COLOUR3 + """;} """)
        self.bottomLayout.addWidget(label, 2, 1)
        self.profit(totalValue - totalCost)
        self.profitLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bottomLayout.addWidget(self.profitLabel, 2, 2)

        label = QLabel('')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""QWidget{ padding-right: 10px; 
                                        border-left: 1px solid """ + COLOUR3 + """; 
                                        border-bottom: 1px solid """ + COLOUR3 + """;} """)
        self.bottomLayout.addWidget(label, 3, 1)
        self.percentProfit(totalPercentProfit)
        self.percentProfitLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bottomLayout.addWidget(self.percentProfitLabel, 3, 2)

    def profit(self, profit):
        if profit > 0:
            self.profitLabel.setStyleSheet(
                """QWidget{ color: """ + GREEN + """; 
                            padding-right: 10px; 
                            border-left: 1px solid """ + COLOUR3 + """; 
                            border-bottom: 1px solid """ + COLOUR3 + """; 
                            border-right: 1px solid """ + COLOUR3 + """;} """)
            profitTextFormat = '${:.2f}'
        else:
            self.profitLabel.setStyleSheet(
                """QWidget{ color: """ + RED + """ 
                            padding-right: 10px; 
                            border-left: 1px solid """ + COLOUR3 + """; 
                            border-bottom: 1px solid """ + COLOUR3 + """; 
                            border-right: 1px solid """ + COLOUR3 + """;} """)
            profitTextFormat = '-${:.2f}'
        self.profitLabel.setText(profitTextFormat.format(abs(profit)))

    def percentProfit(self, percentProfit):
        self.percentProfitLabel.setText('{:.2f}%'.format(percentProfit))
        if percentProfit > 0:
            self.percentProfitLabel.setStyleSheet("""QWidget{ color: """ + GREEN + """; 
                                                              padding-right: 25px; 
                                                              border-right: 1px solid """ + COLOUR3 + """; 
                                                              border-left: 1px solid """ + COLOUR3 + """; 
                                                              border-bottom: 1px solid """ + COLOUR3 + """;}""")
        else:
            self.percentProfitLabel.setStyleSheet("""QWidget{ color: """ + RED + """; 
                                                              padding-right: 25px; 
                                                              border-right: 1px solid """ + COLOUR3 + """; 
                                                              border-left: 1px solid """ + COLOUR3 + """; 
                                                              border-bottom: 1px solid """ + COLOUR3 + """;}""")
