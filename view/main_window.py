from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMainWindow, QGridLayout, QDesktopWidget, QScrollArea, QWidget, QSpacerItem, \
    QSizePolicy, QLabel

from control.config import COLOUR0, COLOUR1, COLOUR2, COLOUR3
from view.download_window import DownloadWindow
from view.ui_elements import buffButton


class MainWindow(QMainWindow):

    def __init__(self, fatController):
        super(MainWindow, self).__init__(fatController)
        self.fatController = fatController
        self.view = fatController.view
        self.portfolio = self.fatController.model.portfolio
        self.progressDialog = DownloadWindow()
        self.progressDialog.hide()

        self.ui()

    def ui(self):
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, 1300, screen.height())
        self.setContentsMargins(0, 0, 0, 0)

        self.view.topLayout.setContentsMargins(0, 0, 0, 0)
        self.view.topLayout.setSpacing(0)
        topWidget = QWidget()
        topWidget.setStyleSheet("""QWidget {background-color: """ + COLOUR1 + """;}""")
        topWidget.setLayout(self.view.topLayout)
        topWidgetScroll = QScrollArea()
        topWidgetScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        topWidgetScroll.setWidgetResizable(True)
        topWidgetScroll.setWidget(topWidget)
        topWidgetScroll.setStyleSheet("""QScrollBar:vertical {border: 1px solid """ + COLOUR2 + """;
                                                              background: """ + COLOUR1 + """;
                                                              width:10px;
                                                              margin: 0px 0px 0px 0px;}""")

        for stock in self.portfolio:
            self.view.createPanel(stock)

        self.view.bottomLayout.setContentsMargins(0, 0, 0, 0)
        self.view.bottomLayout.setSpacing(0)
        bottomWidget = QWidget()
        bottomWidget.setFixedHeight(200)
        bottomWidget.setStyleSheet("""QWidget {color: """ + COLOUR3 + """; background-color: """ + COLOUR0 + """;}""")
        bottomWidget.setLayout(self.view.bottomLayout)

        self.view.createTotalsPanel()

        self.view.sideLayout.setContentsMargins(0, 0, 0, 0)
        self.view.sideLayout.setSpacing(5)

        self.view.sideLayout.addWidget(buffButton('Help',
                                                  50,
                                                  False,
                                                  COLOUR1,
                                                  COLOUR1,
                                                  COLOUR3,
                                                  COLOUR3,
                                                  self.fatController.view.help))
        self.view.sideLayout.addWidget(buffButton('Config',
                                                  50,
                                                  False,
                                                  COLOUR1,
                                                  COLOUR1,
                                                  COLOUR3,
                                                  COLOUR3,
                                                  self.fatController.view.config))
        self.view.sideLayout.addWidget(buffButton('Live',
                                                  50,
                                                  False,
                                                  COLOUR1,
                                                  COLOUR1,
                                                  COLOUR3,
                                                  COLOUR3,
                                                  self.fatController.model.readAllLive))
        self.view.sideLayout.addWidget(buffButton('Quit',
                                                  50,
                                                  False,
                                                  COLOUR1,
                                                  COLOUR1,
                                                  COLOUR3,
                                                  COLOUR3,
                                                  self.fatController.quitApp))
        self.view.sideLayout.addWidget(self.progressDialog)
        self.view.sideLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        sideWidget = QWidget()
        sideWidget.setFixedSize(55, 980)
        sideWidget.setStyleSheet("""QWidget {background-color: """ + COLOUR0 + """;}""")
        sideWidget.setLayout(self.view.sideLayout)

        centralWidget = QWidget()
        centralLayout = QGridLayout()
        centralWidget.setLayout(centralLayout)
        centralLayout.addWidget(topWidgetScroll, 0, 1, 1, 1)
        centralLayout.addWidget(sideWidget, 0, 0, 2, 1)
        centralLayout.addWidget(bottomWidget, 1, 1, 1, 1)
        self.setCentralWidget(centralWidget)

        self.setStyleSheet("""QMainWindow {background-color: """ + COLOUR0 + """;}""")
        self.setAutoFillBackground(True)
        self.setWindowTitle('Buffetizer')
