# ---------------------------------------------------------------------------- #
## \file panel.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty
from bsocket import *
from colors import Colors
from block import Block
from tetris import Tetris
from g import G


class Panel(Widget):
    score = NumericProperty(-1)
    smooth = BooleanProperty(True)
    pause = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Panel, self).__init__(**kwargs)
        _, self.y_min = self.pos
        self.bs = self.size[1] // 20
        self.dev_buttons = list()
        if len(BSocket.paired()) == 0:
            self.ids.server_button.opacity = 0.5
            self.ids.client_button.opacity = 0.5
        self.wall(self.bs * 3)
        print('panel::__init__ pos={} size={} bs={}'.format(
            self.pos, self.size, self.bs))
        G.root.add_widget(self)

    def wall(self, x):
        with self.canvas:
            c1 = Colors.color1(Colors.GREY)
            c2 = Colors.color2(Colors.GREY)
            c3 = Colors.color3(Colors.GREY)
            for i in range(0, 20):
                Block(c1=c1,
                      c2=c2,
                      c3=c3,
                      pos=(x, self.bs * i + self.y_min),
                      size=(self.bs, self.bs))

    def new_tetris(self):
        for i in range(1, 3):
            if G.tetris[i] is None:
                G.tetris[i] = Tetris(pos=(self.bs * (i * 11 + 4), self.y_min),
                                     size=(self.bs * 10, self.bs * 20))
                return

    def on_start_button(self):
        self.ids.start_button.opacity = 0.5
        self.ids.server_button.opacity = 0
        self.ids.client_button.opacity = 0
        self.ids.server_button_2.opacity = 0
        self.ids.client_button_2.opacity = 0
        self.score = 0
        G.send('c')
        G.tetris[0].start()

    def on_pause_button(self):
        self.apply_pause(not self.pause)
        G.send('p{}'.format(1 if self.pause else 0))

    def apply_pause(self, p):
        G.tetris[0].paused = p
        self.pause = p

    def stop(self):
        self.ids.start_button.opacity = 1

    def on_pressButtons(self):
        if self.ids.server_button.opacity > 0:
            self.ids.server_button.opacity = 0.75
        if self.ids.client_button.opacity > 0:
            self.ids.client_button.opacity = 0.75

    def on_pressButtons2(self):
        if self.ids.server_button_2.opacity > 0:
            self.ids.server_button_2.opacity = 0.75
        if self.ids.client_button_2.opacity > 0:
            self.ids.client_button_2.opacity = 0.75

    def on_pressDevButtons(self, button):
        for i in self.dev_buttons:
            i.opacity = 0.5

    def on_connect(self, server, index):
        if index == 1:
            self.ids.server_button.opacity = 0.5
            self.ids.client_button.opacity = 0.5
        elif server:
            self.ids.server_button_2.opacity = 0.5
        else:
            self.ids.client_button_2.opacity = 0.5
        if G.socket[index] is None:
            G.socket[index] = BSocket.instance()
        if server:
            if G.socket[index].listen():
                self.new_tetris()
                if index == 1:
                    self.ids.server_button.opacity = 0
                    self.ids.client_button.opacity = 0
                    self.ids.client_button_2.opacity = 1
                else:
                    self.ids.server_button_2.opacity = 0
            else:
                if index == 1:
                    self.ids.server_button.opacity = 1
                    self.ids.client_button.opacity = 1
                else:
                    self.ids.server_button_2.opacity = 1
        else:
            n = 1
            for device in BSocket.paired():
                button = Button(text=device[0],
                                pos=(self.bs * (11 * index + 6),
                                     self.bs * (13 - 3 * n)),
                                size=(self.bs * 6, self.bs * 2),
                                font_size=self.bs >> 1)
                button.bind(on_press=self.on_pressDevButtons)
                button.bind(on_release=self.on_create)
                self.add_widget(button)
                self.dev_buttons.append(button)
                n += 1
                if n > 2:
                    return

    def on_create(self, button):
        i = 2
        while G.socket[i] is None:
            i -= 1
        if i > 0 and G.socket[i].create(name=button.text):
            self.new_tetris()
            if i == 1:
                self.ids.server_button.opacity = 0
                self.ids.client_button.opacity = 0
                self.ids.server_button_2.opacity = 1
            else:
                self.ids.client_button_2.opacity = 0
        else:
            if i == 1:
                self.ids.server_button.opacity = 1
                self.ids.client_button.opacity = 1
            else:
                self.ids.client_button_2.opacity = 1
        for i in self.dev_buttons:
            self.remove_widget(i)
        self.dev_buttons.clear()

    def on_smooth_button(self):
        self.smooth = not self.smooth
        G.tetris[0].smooth(self.smooth)
