# ---------------------------------------------------------------------------- #
## \file block.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
from kivy.uix.widget import Widget
from kivy.properties import ColorProperty


class Block(Widget):
    c1 = ColorProperty()
    c2 = ColorProperty()
    c3 = ColorProperty()
