'''
Created on 4 Jul. 2020

@author: mullsy
'''
import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel

from controller import FatController


class TestWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.row = 0
        self.ui()
        
    def ui(self):
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        
        for x in range(0, 5):
            print(x)
            self.createPanel(x)
            
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)

        self.setCentralWidget(centralWidget)

        self.setStyleSheet("""QMainWindow {background-color: 'red';}""")
        self.setAutoFillBackground(True)
        self.setWindowTitle('Buffetizer')

    def createPanel(self, x):
        panel = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(0,2,0,0)
        layout.setSpacing(0)
        panel.setLayout(layout)

        layout.addWidget(QLabel('Cost'), 0, 0)
        layout.addWidget(QLabel('$2300'), 0, 1)
        layout.addWidget(QLabel('Held'), 1, 0)
        layout.addWidget(QLabel('1098'), 1, 1)
        layout.addWidget(QLabel('Profit'), 2, 0)
        layout.addWidget(QLabel('$5409'), 2, 1)
        layout.addWidget(QLabel('%Profit'), 3, 0)
        layout.addWidget(QLabel('60%'), 3, 1)

        panel.setStyleSheet("""QWidget{background-color: """ + '#{}{}{}'.format(x, x+5, 9) + """;}""")
        self.layout.addWidget(panel, x, 0)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
#     w = TestWindow()
    controller = FatController()

    sys.exit(app.exec_())