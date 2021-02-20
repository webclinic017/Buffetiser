import os

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGridLayout, QLabel, QDialogButtonBox, QSizePolicy, QSpacerItem, \
    QDialog, QScrollArea, QWidget

from control.config import COLOUR0, COLOUR3, COLOUR2, COLOUR1


class ConfigDialog(QDialog):

    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""QDialog{background-color: """ + COLOUR0 + """;} """)

        layout = QGridLayout()

        configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.csv'))
        configValues = open(configPath, 'r').read().split('\n')

        iconLabel = QLabel()
        pixmap = QPixmap('media/icon.png').scaled(128, 128, transformMode=Qt.SmoothTransformation)
        iconLabel.setPixmap(pixmap)
        iconLabel.setStyleSheet("""QLabel { padding-left: 100;""")
        layout.addWidget(iconLabel, 0, 0, 2, 1)

        dataIconLabel = QLabel()
        pixmap = QPixmap('media/eod.png').scaled(60, 60, transformMode=Qt.SmoothTransformation)
        dataIconLabel.setPixmap(pixmap)
        dataLabel = QLabel('''Get a fully functional and free <br>API Key from ''' +
                           '''<a style="color: ''' +
                           COLOUR3 +
                           ''';" href='https://eodhistoricaldata.com'>EOD Historical Data</a>''')
        dataLabel.setStyleSheet("""QLabel{ padding-left: 100;
                                           background-color: """ + COLOUR0 + """;
                                           color: """ + COLOUR2 + """;}""")
        dataLabel.setOpenExternalLinks(True)
        layout.addWidget(dataLabel, 0, 1)
        layout.addWidget(dataIconLabel, 0, 2)

        currencyConverterIconLabel = QLabel()
        pixmap = QPixmap('media/forex.png').scaled(50, 50, transformMode=Qt.SmoothTransformation)
        currencyConverterIconLabel.setPixmap(pixmap)
        currencyConverterLabel = QLabel('''Currency Conversion by ''' +
                                        '''<a style = "color: ''' +
                                        COLOUR3 +
                                        '''; "href='https://www.freeforexapi.com'>Forex</a>''')
        currencyConverterLabel.setStyleSheet("""QLabel{ padding-left: 100;
                                                        background-color: """ + COLOUR0 + """;
                                                        color: """ + COLOUR2 + """;}""")
        currencyConverterLabel.setOpenExternalLinks(True)
        layout.addWidget(currencyConverterLabel, 1, 1)
        layout.addWidget(currencyConverterIconLabel, 1, 2)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 0)

        investmentsHeldWidget = QWidget()
        investmentsHeldWidget.setStyleSheet("""QWidget {background-color: """ + COLOUR1 + """;
                                                        color: """ + COLOUR3 + """}""")
        investmentsHeldLayout = QGridLayout()
        investmentsHeldScroll = QScrollArea()
        investmentsHeldWidget.setLayout(investmentsHeldLayout)
        investmentsHeldScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        investmentsHeldScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        investmentsHeldScroll.setWidgetResizable(True)
        investmentsHeldScroll.setWidget(investmentsHeldWidget)
        investmentsHeldScroll.setStyleSheet("""QScrollArea {border: 1px solid """ + COLOUR2 + """;
                                                                      background: """ + COLOUR1 + """;
                                                                      width:10px;
                                                                      margin: 0px 0px 0px 0px;}""")

        htmlText = '<html><table width="100%"><tr><th>Code</th><th>Name</th><th>Held</th><th>Cost</th><tr></tr>'
        for line in configValues[2:-1]:
            cells = line.split(',')
            htmlText += '<tr><td>' + cells[1] + \
                        '</td><td>' + cells[2] + \
                        '</td><td>' + cells[3] + \
                        '</td><td>' + cells[4] + '</td></tr>'
        htmlText += '</table></html>'
        htmlLabel = QLabel(htmlText)
        htmlLabel.setStyleSheet("""QLabel{border: 1px solid black;}""")
        investmentsHeldLayout.addWidget(htmlLabel, 3, 0, 1, 6)

        layout.addWidget(investmentsHeldWidget, 3, 0, 1, 6)

        buttonBox = QDialogButtonBox(self)
        buttonBox.addButton("OK", QDialogButtonBox.AcceptRole)
        buttonBox.accepted.connect(self.closeDialog)
        buttonBox.rejected.connect(self.closeDialog)
        layout.addWidget(buttonBox, 4, 3, 1, 3)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 5, 0)

        self.setLayout(layout)

    def closeDialog(self):
        self.hide()
