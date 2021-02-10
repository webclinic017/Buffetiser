from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QGridLayout, QDesktopWidget, QScrollArea, QWidget, QSpacerItem, \
    QSizePolicy

from view.ui_elements import buffButton


class MainWindow(QMainWindow):

    def __init__(self, fatController):
        super(MainWindow, self).__init__(fatController)

        self.fatController = fatController
        self.view = fatController.view
        self.portfolio = self.fatController.model.portfolio

        self.ui()

    def ui(self):

        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, 1300, screen.height())
        self.setContentsMargins(0, 0, 0, 0)

        self.view.topLayout.setContentsMargins(0, 0, 0, 0)
        self.view.topLayout.setSpacing(0)
        topWidget = QWidget()
        topWidget.setStyleSheet("""QWidget {background-color: '#DDD';}""")
        topWidget.setLayout(self.view.topLayout)
        topWidgetScroll = QScrollArea()
        topWidgetScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        topWidgetScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        topWidgetScroll.setWidgetResizable(True)
        topWidgetScroll.setWidget(topWidget)

        for stock in self.portfolio:
            self.view.createPanel(stock)

        self.view.bottomLayout.setContentsMargins(0, 0, 0, 0)
        self.view.bottomLayout.setSpacing(0)
        bottomWidget = QWidget()
        bottomWidget.setFixedHeight(200)
        bottomWidget.setStyleSheet("""QWidget {background-color: '#FFF';}""")
        bottomWidget.setLayout(self.view.bottomLayout)

        self.view.createTotalsPanel()

        self.view.sideLayout.setContentsMargins(0, 0, 0, 0)
        self.view.sideLayout.setSpacing(5)
        self.view.sideLayout.addWidget(buffButton('Config', 50, False, 'white', '#DDD', self.fatController.view.config))
        self.view.sideLayout.addWidget(buffButton('Live', 50, False, 'white', '#DDD', self.fatController.model.readAllLive))
        self.view.sideLayout.addWidget(buffButton('Quit', 50, False, 'white', '#DDD', self.fatController.quitApp))
        verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.view.sideLayout.addItem(verticalSpacer)
        for stock in self.portfolio:
            self.view.sideLayout.addWidget(buffButton(stock.code,
                                                      20,
                                                      True,
                                                      'rgb(0, 144, 23)',
                                                      '#DDD',
                                                      self.fatController.model.totalsStock))

        sideWidget = QWidget()
        sideWidget.setFixedSize(50, 980)
        sideWidget.setStyleSheet("""QWidget {background-color: '#DD0';}""")
        sideWidget.setLayout(self.view.sideLayout)

        centralWidget = QWidget()
        centralLayout = QGridLayout()
        centralWidget.setLayout(centralLayout)
        centralLayout.addWidget(topWidgetScroll, 0, 1, 1, 1)
        centralLayout.addWidget(sideWidget, 0, 0, 2, 1)
        centralLayout.addWidget(bottomWidget, 1, 1, 1, 1)
        self.setCentralWidget(centralWidget)

        self.setStyleSheet("""QMainWindow {background-color: '#DDD';}""")
        self.setAutoFillBackground(True)
        self.setWindowTitle('Buffetizer')