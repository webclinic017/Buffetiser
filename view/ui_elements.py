from PySide2.QtWidgets import QPushButton


def buffButton(text, height, toggle, offColour, onColour, function):
    genericButton = QPushButton(text)
    genericButton.setFixedSize(50, height)
    genericButton.setCheckable(True)
    genericButton.clicked.connect(lambda: function(text))
    if toggle:
        genericButton.setStyleSheet("""QPushButton {background-color: """ + offColour + """; 
                                       border: 1px solid #555; color: white;}
                                       QPushButton::checked{background: """ + onColour + """; 
                                       color: white;}""")
    else:
        genericButton.setStyleSheet("""QPushButton {background-color: """ + offColour + """; 
                                       border: 1px solid #555;}
                                       QPushButton::pressed{background: """ + onColour + """; 
                                       color: white;}""")
    return genericButton






