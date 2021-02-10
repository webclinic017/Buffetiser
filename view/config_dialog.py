import os

from PySide2.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QDialogButtonBox, QSizePolicy, QSpacerItem, \
    QDialog


class ConfigDialog(QDialog):

    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setFixedSize(500, 350)
        self.setStyleSheet("""QDialog{background-color: white;} """)

        layout = QGridLayout()

        configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.csv'))
        configValues = open(configPath, 'r').read().split('\n')
        linkLabel = QLabel('''Get a fully functional and free API Key from 
                              <a href='https://eodhistoricaldata.com'>EOD Historical Data</a>''')
        linkLabel.setOpenExternalLinks(True)
        layout.addWidget(linkLabel, 0, 0, 1, 6)
        apiKey = QLineEdit(configValues[0])
        layout.addWidget(apiKey, 1, 1, 1, 4)

        layout.addWidget(QLabel('Add new stock:'), 2, 0, 1, 1)
        codeText = QLineEdit('Code')
        layout.addWidget(codeText, 2, 1, 1, 1)
        nameText = QLineEdit('Name')
        layout.addWidget(nameText, 2, 2, 1, 1)
        heldText = QLineEdit('Held')
        layout.addWidget(heldText, 2, 3, 1, 1)
        costText = QLineEdit('Cost')
        layout.addWidget(costText, 2, 4, 1, 1)
        addButton = QPushButton('Add')
        layout.addWidget(addButton, 2, 5, 1, 1)

        htmlText = '<html><table width="100%"><tr><th>Code</th><th>Name</th><th>Held</th><th>Cost</th><tr></tr>'
        for line in configValues[1:-1]:
            cells = line.split(',')
            htmlText += '<tr><td>' + cells[0] + \
                        '</td><td>' + cells[1] + \
                        '</td><td>' + cells[2] + \
                        '</td><td>' + cells[3] + '</td></tr>'
        htmlText += '</table></html>'
        htmlLabel = QLabel(htmlText)
        htmlLabel.setStyleSheet("""QLabel{border: 1px solid black;}""")
        layout.addWidget(htmlLabel, 3, 0, 1, 6)

        buttonBox = QDialogButtonBox(self)
        buttonBox.addButton("OK", QDialogButtonBox.AcceptRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
        buttonBox.accepted.connect(self.writeConfig)
        buttonBox.rejected.connect(self.closeDialog)
        layout.addWidget(buttonBox, 4, 3, 1, 3)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 5, 0)

        self.setLayout(layout)

    def writeConfig(self):
        file = open('config.txt', 'w')
        file.close()
        self.hide()

    def closeDialog(self):
        self.hide()
