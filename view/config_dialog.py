import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, QDialogButtonBox, QSizePolicy, QSpacerItem, \
    QDialog, QScrollArea, QWidget


class ConfigDialog(QDialog):

    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setFixedSize(500, 350)
        self.setStyleSheet("""QDialog{background-color: white;} """)

        layout = QGridLayout()

        configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.csv'))
        configValues = open(configPath, 'r').read().split('\n')
        dataIconLabel = QLabel()
        dataIconLabel.setStyleSheet('''QLabel { background-image: '/Users/mullsy/workspace/Buffetiser/media'} ''''')
        dataLabel = QLabel('''Get a fully functional and free API Key from ''' +
                           '''<a href='https://eodhistoricaldata.com'>EOD Historical Data</a>''')
        dataLabel.setOpenExternalLinks(True)

        layout.addWidget(dataIconLabel, 0, 0, 1, 6)
        layout.addWidget(dataLabel, 0, 0, 1, 6)

        currencyConverterLabel = QLabel('''Currency Conversion by <a href='https://www.freeforexapi.com'>Forex</a>''')
        currencyConverterLabel.setOpenExternalLinks(True)
        layout.addWidget(currencyConverterLabel, 1, 0, 1, 6)

        layout.addWidget(QLabel('To add a new investment, edit the config.csv file.'), 2, 0, 1, 6)

        investmentsHeldWidget = QWidget()
        investmentsHeldLayout = QGridLayout()
        investmentsHeldScroll = QScrollArea()
        investmentsHeldWidget.setLayout(investmentsHeldLayout)
        investmentsHeldScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        investmentsHeldScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        investmentsHeldScroll.setWidgetResizable(True)
        investmentsHeldScroll.setWidget(investmentsHeldWidget)

        htmlText = '<html><table width="100%"><tr><th>Code</th><th>Name</th><th>Held</th><th>Cost</th><tr></tr>'
        for line in configValues[1:-1]:
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
