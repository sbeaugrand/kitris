#!/usr/bin/env python3
# ---------------------------------------------------------------------------- #
## \file main.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.core.window import Window, Keyboard
from kivy.vector import Vector
from kivy.metrics import dp
from kivy.utils import platform
from block import Block
from panel import Panel
from tetris import Tetris
from g import G

if platform != 'android':
    Window.size = (1110, 600)
    #Window.size = (1440, 720)  # pinephone
    #Window.size = (1024, 528)  # klipad
    #Window.size = (960, 504)  # klipad kl600
print(Window.size)
RATE_MIN = 24
RATE_MAX = 60
B_SIZE = ((Window.size[1] // 20) // 6) * 6
Y_MIN = Window.size[1] - B_SIZE * 20
G.initial_frame_rate = B_SIZE
if G.initial_frame_rate > RATE_MAX:
    G.initial_frame_rate >>= 1
if G.initial_frame_rate < RATE_MIN:
    G.initial_frame_rate <<= 1
print('initial_frame_rate = {}'.format(G.initial_frame_rate))


class KitrisApp(App):
    move_event = 0

    def build(self):
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_touch_move=self.on_touch_move)
        Window.bind(on_touch_up=self.on_touch_up)
        G.panel = Panel()
        G.tetris[0] = Tetris(pos=(B_SIZE * 4, Y_MIN),
                             size=(B_SIZE * 10, B_SIZE * 20))
        return G.root

    def on_start(self):
        G.set_rate(G.initial_frame_rate)

    def on_key_down(self, keyboard, keycode, *args):
        if keycode == Keyboard.keycodes['right']:
            G.tetris[0].kx = B_SIZE
        elif keycode == Keyboard.keycodes['left']:
            G.tetris[0].kx = -B_SIZE
        elif keycode == Keyboard.keycodes['up']:
            G.tetris[0].kr = 1
        elif keycode == Keyboard.keycodes['down']:
            G.tetris[0].ky = -111

    def on_touch_move(self, widget, touch):
        if self.move_event == 0:
            v = Vector(touch.pos) - Vector(touch.opos)
        else:
            v = Vector(touch.pos) - Vector(self.move_pos)
        dx, dy = v
        if abs(dx) > abs(dy):
            if v.length() < dp(B_SIZE):
                return True
            if dx < 0:
                G.tetris[0].kx = -B_SIZE
            else:
                G.tetris[0].kx = B_SIZE
            self.move_pos = touch.pos
            self.move_event = 1
        else:
            if v.length() < dp(B_SIZE << 1):
                return True
            if dy < 0:
                G.tetris[0].ky = -111
                self.move_pos = touch.pos
                self.move_event = 1
            elif self.move_event != 2:
                G.tetris[0].kr = 1
                self.move_pos = touch.pos
                self.move_event = 2
        return True

    def on_touch_up(self, widget, touch):
        self.move_event = 0


G.root = Builder.load_string('''
#: import B_SIZE __main__.B_SIZE
#: import Y_MIN __main__.Y_MIN
FloatLayout:

<Panel>:
    pos: 0, Y_MIN
    size: B_SIZE * 4, B_SIZE * 20
    Button:
        id: start_button
        opacity: 1
        text: str(root.score) if root.score >= 0 else 'Start'
        on_press: root.on_start_button() if self.opacity == 1 else None
        pos: 0, B_SIZE * 13 + Y_MIN
        size: B_SIZE * 3, B_SIZE * 2
        bold: True
        font_size: B_SIZE >> 1
    Button:
        id: pause_button
        opacity: 1
        text: 'Resume' if root.pause else 'Pause'
        on_press: root.on_pause_button()
        pos: 0, B_SIZE * 10 + Y_MIN
        size: B_SIZE * 3, B_SIZE * 2
        bold: True
        font_size: B_SIZE >> 1
    Button:
        id: smooth_button
        opacity: 1
        text: 'Smooth on' if root.smooth else 'Smooth off'
        on_press: root.on_smooth_button()
        pos: 0, B_SIZE * 7 + Y_MIN
        size: B_SIZE * 3, B_SIZE * 2
        bold: True
        font_size: B_SIZE >> 1
    Button:
        id: server_button
        opacity: 1
        text: 'Listen'
        on_press: root.on_pressButtons()
        on_release: root.on_connect(server=True, index=1) if self.opacity > 0.5 else None
        pos: B_SIZE * 17, B_SIZE * 16
        size: B_SIZE * 6, B_SIZE * 2
        bold: True
        font_size: B_SIZE >> 1
    Button:
        id: client_button
        opacity: 1
        text: 'Connect'
        on_press: root.on_pressButtons()
        on_release: root.on_connect(server=False, index=1) if self.opacity > 0.5 else None
        pos: B_SIZE * 17, B_SIZE * 13
        size: B_SIZE * 6, B_SIZE * 2
        bold: True
        font_size: B_SIZE >> 1
    Button:
        id: server_button_2
        opacity: 0
        text: 'Listen'
        on_press: root.on_pressButtons2()
        on_release: root.on_connect(server=True, index=2) if self.opacity > 0.5 else None
        pos: B_SIZE * 28, B_SIZE * 16
        size: B_SIZE * 6, B_SIZE * 2
        bold: True
        font_size: B_SIZE >> 1
    Button:
        id: client_button_2
        opacity: 0
        text: 'Connect'
        on_press: root.on_pressButtons2()
        on_release: root.on_connect(server=False, index=2) if self.opacity > 0.5 else None
        pos: B_SIZE * 28, B_SIZE * 13
        size: B_SIZE * 6, B_SIZE * 2
        bold: True
        font_size: B_SIZE >> 1

<Block>:
    size: B_SIZE, B_SIZE
    canvas:
        Color:
            rgb: self.c1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgb: self.c2
        Line:
            points: self.pos[0] + 1, self.pos[1], self.pos[0] + self.size[0] - 1, self.pos[1], self.pos[0] + self.size[0] - 1, self.pos[1] + self.size[1] - 2
        Line:
            points: self.pos[0] + 2, self.pos[1] + 1, self.pos[0] + self.size[0] - 2, self.pos[1] + 1, self.pos[0] + self.size[0] - 2, self.pos[1] + self.size[1] - 3
        Color:
            rgb: self.c3
        Line:
            points: self.pos[0] + self.size[0] - 2, self.pos[1] + self.size[1] - 1, self.pos[0], self.pos[1] + self.size[1] - 1, self.pos[0], self.pos[1] + 1
        Line:
            points: self.pos[0] + self.size[0] - 3, self.pos[1] + self.size[1] - 2, self.pos[0] + 1, self.pos[1] + self.size[1] - 2, self.pos[0] + 1, self.pos[1] + 2
''')

KitrisApp().run()
G.send('x')
G.quit()
