# ---------------------------------------------------------------------------- #
## \file tetrisview.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
import random
from kivy.uix.widget import Widget
from block import Block
from shape import Shape
from colors import Colors
from g import G


class TetrisView(Widget):
    def __init__(self, **kwargs):
        super(TetrisView, self).__init__(**kwargs)
        self.x_min, self.y_min = self.pos
        self.bs = self.size[1] // 20
        self.size_hint = (None, None)
        print('tetrisview::__init__ pos={} size={} bs={}'.format(
            self.pos, self.size, self.bs))
        G.root.add_widget(self)
        G.panel.wall(self.bs * 10 + self.x_min)

    def add_block(self, c, i, j):
        b = Block(c1=Colors.color1(c),
                  c2=Colors.color2(c),
                  c3=Colors.color3(c),
                  pos=(i * self.bs + self.x_min, j * self.bs + self.y_min),
                  size=(self.bs, self.bs))
        self.add_widget(b)
        return b

    def add_grey_block(self, i, j):
        return self.add_block(Colors.GREY, i, j)

    def add_shape(self, i, j, p=None):
        if p is None:
            p = random.randint(0, 6)
        s = Shape(self.bs, p)
        path = s.path()
        s.blocks.append(self.add_block(p, i, j))
        s.blocks.append(self.add_block(p, i + path[0], j + path[1]))
        s.blocks.append(self.add_block(p, i + path[2], j + path[3]))
        s.blocks.append(self.add_block(p, i + path[4], j + path[5]))
        return s
