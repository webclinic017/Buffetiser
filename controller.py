from PySide2.QtWidgets import QWidget

from model.model import Model
from view.view import View


class FatController(QWidget):

    def __init__(self, parent=None):
        super(FatController, self).__init__()

        self.key = 0

        self.model = Model(self)
        self.view = View(self)

        self.model.portfolioSetup()
        self.view.showMainWindow()

    def quitApp(self, exitCode=0):
        self.close()
        exit(exitCode)
