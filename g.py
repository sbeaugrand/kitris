# ---------------------------------------------------------------------------- #
## \file g.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
from kivy.clock import Clock


class G:
    initial_frame_rate = 30
    frame_rate = 30
    clock_event = None
    root = None
    panel = None
    tetris = [None, None, None]
    socket = [None, None, None]

    def set_rate(r=0):
        if r == 0:
            r = G.initial_frame_rate
        G.frame_rate = r
        if G.clock_event is not None:
            G.clock_event.cancel()
        G.clock_event = Clock.schedule_interval(G.tetris[0].update,
                                                1 / G.frame_rate)

    def send(c):
        for i in range(1, 3):
            if G.tetris[i] is not None:
                G.socket[i].send(c)

    def recv():
        for i in range(1, 3):
            if G.tetris[i] is not None:
                if not G.tetris[i].apply(G.socket[i].recv()):
                    G.close(i)

    def close(i):
        G.tetris[i] = None
        print('info: close socket {}'.format(i))
        G.socket[i] = None

    def quit():
        for i in range(1, 3):
            if G.tetris[i] is not None:
                G.close(i)
