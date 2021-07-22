'''
Created on 4 Jul. 2020

@author: mullsy
'''
import os
import sys

from PySide2.QtWidgets import QApplication

from control.controller import FatController

os.environ["QT_MAC_WANTS_LAYER"] = "1"

if __name__ == '__main__':

    app = QApplication(sys.argv)
    controller = FatController()

    sys.exit(app.exec_())

