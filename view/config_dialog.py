import os

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGridLayout, QLabel, QDialogButtonBox, QSizePolicy, QSpacerItem, \
    QDialog, QScrollArea, QWidget, QGraphicsDropShadowEffect

from control.config import COLOUR0, COLOUR3, COLOUR2, COLOUR1, DATA_PATH


class ConfigDialog(QDialog):

    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""QDialog{background-color: """ + COLOUR1 + """;} """)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        configPath = os.path.abspath(DATA_PATH + '/config.csv')
        configValues = open(configPath, 'r').read().split('\n')

        iconLabel = QLabel()
        pixmap = QPixmap('media/icon.png')
        iconLabel.setPixmap(pixmap)
        iconLabel.setStyleSheet("""QLabel {padding-top: 10px;
                                           padding-left: 10;}""")
        layout.addWidget(iconLabel, 0, 0, 6, 1)

        dataLabel = QLabel('''Get a fully functional and free API Key from ''' +
                           '''<a style="color: ''' +
                           COLOUR3 +
                           ''';" href='https://www.weblink.com.au'>WebLink</a>''')
        dataLabel.setStyleSheet("""QLabel{ padding-top: 20px;
                                           padding-left: 60;
                                           padding-bottom: 0px;
                                           margin: 0px;
                                           color: """ + COLOUR3 + """;}""")
        dataIconLabel = QLabel()
        pixmap = QPixmap('media/weblink.png')
        dataIconLabel.setPixmap(pixmap)
        dataIconLabel.setStyleSheet("""QLabel{padding-left: 60;}""")
        dataLabel.setOpenExternalLinks(True)
        layout.addWidget(dataLabel, 0, 1)
        layout.addWidget(dataIconLabel, 1, 1)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 4, 0)
        layout.addWidget(dataLabel, 2, 1)

        currencyConverterLabel = QLabel('''Get free, easy to use Currency Conversion ''' +
                                        '''<a style = "color: ''' +
                                        COLOUR3 +
                                        '''; "href='https://https://www.exchangerate-api.com'>ExchangeRate-API</a>''')
        currencyConverterLabel.setStyleSheet("""QLabel{ padding-left: 60;
                                                        color: """ + COLOUR3 + """;}""")

        currencyConverterLabel.setOpenExternalLinks(True)
        currencyConverterIconLabel = QLabel()
        pixmap = QPixmap('media/hr-logo-2022-rc.png')
        currencyConverterIconLabel.setPixmap(pixmap)
        currencyConverterIconLabel.setStyleSheet("""QLabel{padding-left: 60;}""")
        layout.addWidget(currencyConverterLabel, 3, 1)
        layout.addWidget(currencyConverterIconLabel, 4, 1)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 5, 0)

        investmentsHeldWidget = QWidget()
        investmentsHeldWidget.setStyleSheet("""QWidget {background-color: """ + COLOUR1 + """;
                                                        color: """ + COLOUR3 + """}""")
        investmentsHeldLayout = QGridLayout()
        investmentsHeldWidget.setLayout(investmentsHeldLayout)

        htmlText = '<html><table width="100%"><tr>' \
                   '<th align= "left">Code</th>' \
                   '<th align= "left">Name</th>' \
                   '<th align= "left">Held</th>' \
                   '<th align= "left">Cost</th><tr></tr>'
        for line in configValues[2:-1]:
            cells = line.split(',')
            if cells[0] == 'share' or cells[0] == 'crypto':
                htmlText += '<tr><td>{:2s}</td><td>{:5s}</td><td>{}</td><td>{}</td></tr>'.format(cells[1],
                                                                                                 cells[2],
                                                                                                 cells[3],
                                                                                                 cells[4])
        htmlText += '</table></html>'

        htmlLabel = QLabel(htmlText)
        htmlLabel.setFixedWidth(750)
        htmlLabel.setStyleSheet("""QLabel{border: 1px solid """ + COLOUR2 + """;
                                          padding: 10;}""")
        investmentsHeldLayout.addWidget(htmlLabel, 6, 0, 1, 6)

        scroll = QScrollArea()
        scroll.setFixedWidth(htmlLabel.width() + 30)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""QScrollArea {border: 1px solid """ + COLOUR2 + """;
                                             background: """ + COLOUR1 + """;
                                             margin: 0px 0px 0px 0px;}""")
        scroll.setWidget(investmentsHeldWidget)
        layout.addWidget(scroll, 7, 0, 1, 6)

        buttonBox = QDialogButtonBox(self)
        buttonBox.addButton("OK", QDialogButtonBox.AcceptRole)
        buttonBox.accepted.connect(self.closeDialog)
        buttonBox.rejected.connect(self.closeDialog)
        layout.addWidget(buttonBox, 8, 1, 1, 2)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 5, 0)

        self.setLayout(layout)

    def closeDialog(self):
        self.hide()
