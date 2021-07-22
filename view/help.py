from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QLabel, QGridLayout, QDialog, QDesktopWidget, QPushButton, QDialogButtonBox

from control.config import COLOUR0, COLOUR1


class Help(QDialog):
    def __init__(self, parent=None):
        super(Help, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""QDialog{background-color: """ + COLOUR1 + """;} """)
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, 1300, screen.height())

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        iconLabel = QLabel()
        pixmap = QPixmap('media/icon.png')
        iconLabel.setPixmap(pixmap)
        iconLabel.setStyleSheet("""QLabel {padding-top: 10px;
                                           padding-left: 10;}""")
        layout.addWidget(iconLabel, 0, 0, 6, 1)

        buttonBox = QDialogButtonBox(self)
        buttonBox.addButton("OK", QDialogButtonBox.AcceptRole)
        buttonBox.accepted.connect(self.closeDialog)
        buttonBox.rejected.connect(self.closeDialog)
        layout.addWidget(buttonBox, 11, 1, 1, 2)

        self.setLayout(layout)

    def closeDialog(self):
        self.hide()