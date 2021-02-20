from PySide2.QtWidgets import QPushButton

from control.config import GREEN, COLOUR0, COLOUR3


def buffButton(text, height, toggle, offColour, onColour, textOffColour, textOnColour, function):
    genericButton = QPushButton(text)
    genericButton.setFixedSize(50, height)
    genericButton.setCheckable(True)
    genericButton.clicked.connect(lambda: function(text))
    if toggle:
        genericButton.setStyleSheet("""QPushButton {background-color: """ + offColour + """; 
                                       border: 1px solid """ + COLOUR0 + """;
                                       color: """ + textOffColour + """};
                                       QPushButton::pressed{background: """ + textOnColour + """; 
                                       color: """ + onColour + """};
                                       QPushButton:hover:!pressed{border: 1px solid """ + GREEN + """;}""")
    else:
        genericButton.setStyleSheet("""QPushButton {background-color: """ + offColour + """; 
                                       border: 1px solid """ + COLOUR0 + """;
                                       color: """ + textOffColour + """;}
                                       QPushButton::pressed{background: """ + textOnColour + """; 
                                       color: """ + onColour + """;}
                                       QPushButton:hover:!pressed{border: 1px solid """ + COLOUR3 + """;}""")
    return genericButton
