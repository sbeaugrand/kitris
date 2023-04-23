# ---------------------------------------------------------------------------- #
## \file grid.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
class Grid:
    def __init__(self):
        self.lines = [0 for i in range(0, 24 + 3)]

    def mov_lines_up(self, lines):
        for l in range(23, lines - 1, -1):
            self.lines[l] = self.lines[l - lines]
        for l in range(0, lines):
            self.lines[l] = 0

    def mov_lines_down(self, first):
        for j in range(first, 23):
            self.lines[j] = self.lines[j + 1]
        self.lines[23] = 0

    def is_full(self):
        return self.lines[19] != 0

    def set(self, i, j):
        self.lines[j] |= 1 << i

    def get(self, i, j):
        return self.lines[j] & (1 << i)

    def get_line(self, line):
        return self.lines[line]

    def clear(self):
        for i in range(0, 24 + 3):
            self.lines[i] = 0
