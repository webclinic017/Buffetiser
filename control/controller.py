from PySide2.QtWidgets import QWidget, QDialog, QLabel, QHBoxLayout

from model.model import Model
from view.view import View


class FatController(QWidget):

    def __init__(self):
        super(FatController, self).__init__()

        self.dataSupplier = ''
        self.exchange = 'XASX'
        self.key = 0
        self.currency = 'AUD'
        self.currencyConversionKey = ''
        self.currencyConversion = 1

        self.downloadThread = None

        self.model = Model(self)
        self.view = View(self)

        self.model.portfolioSetup()
        self.view.showMainWindow()

    def showDialog(self, message):
        print(message)
        # dialog = QDialog(self.view.mainWindow)
        # dialog.setFixedSize(400, 100)
        # label = QLabel()
        # label.setText(message)
        # layout = QHBoxLayout()
        # layout.addWidget(label)
        # dialog.setLayout(layout)
        # dialog.show()

    def quitApp(self, exitCode=0):
        if self.downloadThread:
            self.downloadThread.halt = True
        self.close()
        exit(exitCode)
