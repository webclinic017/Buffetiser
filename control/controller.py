from PySide2.QtWidgets import QWidget

from model.model import Model
from view.view import View


class FatController(QWidget):

    def __init__(self):
        super(FatController, self).__init__()

        self.key = 0
        self.usdToAudConversion = 1

        self.downloadThread = None

        self.model = Model(self)
        self.view = View(self)

        self.model.portfolioSetup()
        self.view.showMainWindow()

    def quitApp(self, exitCode=0):
        if self.downloadThread:
            self.downloadThread.halt = True
        self.close()
        exit(exitCode)
