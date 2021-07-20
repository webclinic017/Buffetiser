# Colours
import os
from pathlib import Path

import pygal.style

RED = 'red'
GREEN = '#5B5'

COLOUR0 = '#1B262C'
COLOUR1 = '#0f4c75'
COLOUR2 = '#3282b8'
COLOUR3 = '#bbe1fa'

'''
Default: pygal.style.DefaultStyle
DarkStyle: pygal.style.DarkStyle
Neon: pygal.style.NeonStyle
Dark Solarized: pygal.style.DarkSolarizedStyle
Light Solarized: pygal.style.LightSolarizedStyle
Light: pygal.style.LightStyle
Clean: pygal.style.CleanStyle
Red Blue: pygal.style.RedBlueStyle
Dark Colorized: pygal.style.DarkColorizedStyle
Light Colorized: pygal.style.LightColorizedStyle
Turquoise: pygal.style.TurquoiseStyle
Light green: pygal.style.LightGreenStyle
Dark green: pygal.style.DarkGreenStyle
Dark green blue: pygal.style.DarkGreenBlueStyle
Blue: pygal.style.BlueStyle
'''
INVESTMENT_PLOT_STYLE = pygal.style.DarkStyle
TOTALS_PLOT_STYLE = pygal.style.DarkStyle

# This is where the data directory will be located. Should be in user's home.
DATA_PATH = str(os.path.join(Path.home(), 'buffetiser'))

SHOW_LOW = True
SHOW_HIGH = True
SHOW_CLOSE = True
