# ---------------------------------------------------------------------------- #
## \file shape.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
class Shape():
    def __init__(self, bs, p):
        self.bs = bs
        self.p = p
        path = self.path()
        self.rotation = 0
        self.blocks = list()

    def move(self, u, v):
        for i in self.blocks:
            i.pos = (i.pos[0] + u, i.pos[1] + v)

    def moveto(self, x, y):
        self.move(x - self.blocks[0].pos[0], y - self.blocks[0].pos[1])

    def rotate(self, d):
        self.rotation += d
        if self.rotation > 3:
            self.rotation = 0
        elif self.rotation < 0:
            self.rotation = 3
        path = self.path()
        x, y = (-1, -1)
        j = 0
        for i in self.blocks:
            if x < 0:
                x, y = i.pos
            else:
                if self.rotation == 0:
                    i.pos = (x + path[j] * self.bs, y + path[j + 1] * self.bs)
                elif self.rotation == 1:
                    i.pos = (x - path[j + 1] * self.bs, y + path[j] * self.bs)
                elif self.rotation == 2:
                    i.pos = (x - path[j] * self.bs, y - path[j + 1] * self.bs)
                else:
                    i.pos = (x + path[j + 1] * self.bs, y - path[j] * self.bs)
                j += 2

    def path(self):
        return (
            (-0, 1, -0, 2, 0, -1),  # I
            (1, -0, 1, -1, 0, -1),  # O
            (-1, -0, 0, -1, 1, 0),  # T
            (-0, -1, 0, 1, -1, 1),  # L
            (-0, -1, -0, 1, 1, 1),  # J
            (-1, 1, -1, 0, 0, -1),  # S
            (1, 1, 1, -0, -0, -1),  # Z
        )[self.p]
