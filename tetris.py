# ---------------------------------------------------------------------------- #
## \file tetris.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
import random
from grid import Grid
from tetrisview import TetrisView
from sfx import Sfx
from g import G


class Tetris():
    def __init__(self, pos, size):
        self.x_min, self.y_min = pos
        self.bs = size[1] // 20
        self.view = TetrisView(pos=pos, size=size)
        self.shapes = list()
        self.shape = None
        self.nexts = None
        self.kx = 0
        self.ky = 0
        self.kr = 0
        self.started = False
        self.paused = False
        self.speed = 2
        self.count = 0
        self.freq = 1
        self.grid = Grid()
        self.recv_freq = self.bs // 3
        self.recv_count = 0

    def smooth(self, s):
        started = self.started
        self.started = False
        if s:
            G.set_rate()
            self.freq = 1
        else:
            G.set_rate(6)
            self.freq = 3
        self.count = self.freq
        self.reset_keys()
        self.shape.move(0,
                        -(self.shape.blocks[0].pos[1] - self.y_min) % self.bs)
        self.started = started

    def new_shape(self):
        if self.nexts is None:
            self.nexts = self.view.add_shape(1 - self.x_min // self.bs, 17)
        self.shape = self.nexts
        x = self.bs * 4 + self.x_min
        y = self.bs * 21 + self.y_min
        p = self.shape.p
        if p == 0 or p == 2 or p == 3 or p == 5:
            x += self.bs
        self.shape.moveto(x, y)
        self.nexts = self.view.add_shape(1 - self.x_min // self.bs, 17)
        self.collisions = 0
        self.reset_keys()
        G.send('s{}'.format(p))

    def apply(self, lst):
        while lst:
            buf = lst.pop(0)
            #print(buf)
            try:
                if buf[0] == 's':
                    p = int(buf[1])
                    x = 4
                    y = 21
                    if p == 0 or p == 2 or p == 3 or p == 5:
                        x += 1
                    self.shape = self.view.add_shape(x, y, p=p)
                    self.started = True
                elif buf[0] == 'r':
                    r = int(buf[1])
                    self.shape.rotate(r - self.shape.rotation)
                elif buf[0] == 'd':
                    n = self.del_lines()
                    if n != int(buf[1]):
                        print('error: del_lines {} != {}'.format(
                            n, int(buf[1])))
                        Sfx.error()
                elif buf[0] == 'c':
                    self.apply_start()
                elif buf[0] == 'a':
                    G.tetris[0].apply_send_lines(int(buf[1]))
                elif buf[0] == 'u':
                    self.add_lines(int(buf[1]), int(buf[2]))
                elif buf[0] == 'p':
                    G.tetris[0].apply_pause(int(buf[1]))
                elif buf[0] == 'i':
                    print(buf[1:])
                elif buf[0] == 'e':
                    if not self.started:
                        print('apply: already stoped')
                    self.started = False
                elif buf[0] == 'x':
                    return False
                else:
                    x = int(buf[0]) * self.bs + self.x_min
                    y = (int(buf[1]) * 10 + int(buf[2])) * self.bs + self.y_min
                    self.shape.moveto(x, y)
            except Exception as e:
                print(buf)
                print('apply: {}'.format(e))
        return True

    def mov_lines(self, lines):
        self.grid.mov_lines_up(lines)
        if self.shape is not None:
            for k in self.shape.blocks:
                k.pos = (k.pos[0], k.pos[1] + self.bs * lines)
        for j in self.shapes:
            for k in j:
                k.pos = (k.pos[0], k.pos[1] + self.bs * lines)
        if self.grid.is_full():
            self.started = False
            G.panel.stop()

    def collision(self):
        if self.dx != 0:
            for b in self.shape.blocks:
                x = b.pos[0] - self.x_min
                y = b.pos[1] - self.y_min
                if x + self.dx < 0:
                    self.dx = 0
                    break
                if x + self.dx >= self.bs * 10:
                    self.dx = 0
                    break
                i = (x + self.dx) // self.bs
                j, m = divmod(y, self.bs)
                if self.grid.get(i, j):
                    self.dx = 0
                    break
                elif m > 0 and self.grid.get(i, j + 1):
                    self.dx = 0
                    break
        if self.dy != 0:
            for b in self.shape.blocks:
                x = b.pos[0] - self.x_min
                y = b.pos[1] - self.y_min
                if y + self.dy < 0:
                    self.dy = 0
                    return True
                i = (x + self.dx) // self.bs
                j, m = divmod(y + self.dy, self.bs)
                if self.grid.get(i, j):
                    self.dy = 0
                    return True
                elif m > 0 and self.grid.get(i, j + 1):
                    self.dy = 0
                    return True
        return False

    def contact(self):
        for b in self.shape.blocks:
            x = b.pos[0] - self.x_min
            y = b.pos[1] - self.y_min - self.bs
            if y < 0:
                return True
            i = x // self.bs
            j = y // self.bs
            if self.grid.get(i, j):
                return True
        return False

    def rotate(self):
        self.shape.rotate(self.kr)
        for b in self.shape.blocks:
            x = b.pos[0] - self.x_min
            y = b.pos[1] - self.y_min
            if y < 0:
                return False
            if x < 0:
                return False
            if x >= self.bs * 10:
                return False
            i = x // self.bs
            j, m = divmod(y + self.dy, self.bs)
            if self.grid.get(i, j):
                return False
            elif m > 0 and self.grid.get(i, j + 1):
                return False
        return True

    def del_blocks(self, y):
        count = 0
        while True:
            for j in self.shapes:
                for k in j:
                    if k.pos[1] == y:
                        self.view.remove_widget(k)
                        j.remove(k)
                        count += 1
                        if count == 10:
                            return

    def del_lines(self):
        lines = 0
        for b in self.shape.blocks:
            i = (b.pos[0] - self.x_min) // self.bs
            j = (b.pos[1] - self.y_min) // self.bs
            self.grid.set(i, j)
        self.shapes.append(self.shape.blocks)
        self.shape = None
        #for i in range(0, 20):
        #    print('{:10b}'.format(self.grid.lines[i]))
        for i in range(0, 20):
            y = i * self.bs + self.y_min
            while self.grid.get_line(i) == 0b1111111111:
                self.del_blocks(y)
                self.grid.mov_lines_down(i)
                for j in self.shapes:
                    for k in j:
                        if k.pos[1] > y:
                            k.pos = (k.pos[0], k.pos[1] - self.bs)
                lines += 1
        return lines

    def send_lines(self, lines):
        if lines < 2:
            return
        lines -= 1
        n = 0
        if G.tetris[1] is not None and G.tetris[1].started:
            n += 1
        if G.tetris[2] is not None and G.tetris[2].started:
            n += 2
        if n == 0:
            return
        elif n < 3:
            i = n
        else:
            i = random.randint(0, 1) + 1
        G.socket[i].send('a{}'.format(lines))

    def add_lines(self, lines, k):
        self.mov_lines(lines)
        blocks = list()
        for j in range(0, lines):
            for i in range(0, 10):
                if i != k:
                    self.grid.set(i, j)
                    blocks.append(self.view.add_grey_block(i, j))
        self.shapes.append(blocks)

    def apply_send_lines(self, lines):
        k = random.randint(0, 9)
        self.add_lines(lines, k)
        G.send('u{}{}'.format(lines, k))

    def reset_keys(self):
        self.kx = 0
        if self.count == self.freq:
            self.count = 0
            self.ky = -((self.bs * self.speed * self.freq) // G.frame_rate)

    def apply_start(self):
        self.grid.clear()
        self.view.clear_widgets()
        if self.shapes is not None:
            self.shapes.clear()

    def apply_pause(self, p):
        G.panel.apply_pause(p)

    def start(self):
        self.apply_start()
        if self.nexts is not None:
            for i in self.nexts.blocks:
                self.view.add_widget(i)
        self.new_shape()
        self.count = 0
        self.started = True
        Sfx.start()

    def fall(self):
        self.ky = -(self.shape.blocks[0].pos[1] % self.bs)
        if self.ky == 0:
            self.ky = -self.bs
        self.dy = self.ky
        while not self.collision():
            self.ky -= self.bs
            self.dy = self.ky
        self.dy = self.ky + self.bs
        if self.dy > 0:
            self.dy = 0

    def end_collision(self):
        l = self.del_lines()
        G.panel.score += l
        G.send('d{}'.format(l))
        self.send_lines(l)
        if l > 0:
            Sfx.lines(l)
        if self.grid.is_full():
            self.started = False
            G.panel.stop()
            Sfx.pause()
            G.send('e')
        else:
            self.new_shape()

    def update(self, dt):
        self.recv_count += 1
        if self.recv_count > self.recv_freq:
            self.recv_count = 0
            G.recv()
        if not self.started or self.paused:
            return
        self.count += 1
        if self.kr > 0:
            if not self.rotate():
                self.shape.rotate(-self.kr)
            else:
                Sfx.rotate()
            self.kr = 0
            G.send('r{}'.format(self.shape.rotation))
        self.dx = self.kx
        if self.ky == -111:
            self.fall()
            self.collisions += 1
            if self.dy < -(self.bs << 3):
                Sfx.fall()
            else:
                Sfx.landing()
        else:
            if self.count < self.freq:
                if self.dx == 0:
                    self.reset_keys()
                    return
                self.dy = 0
            else:
                self.dy = self.ky
            if self.collision():
                self.collisions += 1
                if (self.count == self.freq and self.collisions >=
                    (G.frame_rate << 1) // (self.freq + 1)):
                    self.end_collision()
                    return
                if self.dx != 0:
                    self.collisions = 0
            else:
                self.collisions = 0
        if self.dx != 0 or self.dy != 0:
            self.shape.move(self.dx, self.dy)
            if self.dx != 0:
                Sfx.move()
            x, y = self.shape.blocks[0].pos
            if (y - self.y_min) % self.bs == 0:
                G.send('{}{:02}'.format((x - self.x_min) // self.bs,
                                        (y - self.y_min) // self.bs))
        if (self.dy != 0 and self.collisions == 0 and self.count == self.freq
                and (self.shape.blocks[0].pos[1] - self.y_min) % self.bs == 0
                and self.contact()):
            Sfx.landing()
        self.reset_keys()
