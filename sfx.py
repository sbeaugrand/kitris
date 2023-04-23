# ---------------------------------------------------------------------------- #
## \file sfx.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
from kivy.core.audio import SoundLoader


class Sfx:
    sound_start = SoundLoader.load('data/se_sys_ok.wav')
    sound_pause = SoundLoader.load('data/se_game_pause.wav')
    sound_rotate = SoundLoader.load('data/se_game_rotate.wav')
    sound_fall = SoundLoader.load('data/se_game_bfall.wav')
    sound_landing = SoundLoader.load('data/se_game_landing.wav')
    sound_move = SoundLoader.load('data/se_game_move.wav')
    sound_error = SoundLoader.load('data/se_game_caution.wav')
    sound_single = SoundLoader.load('data/se_game_single.wav')
    sound_double = SoundLoader.load('data/se_game_double.wav')
    sound_triple = SoundLoader.load('data/se_game_triple.wav')
    sound_tetris = SoundLoader.load('data/se_game_tetris.wav')

    def start():
        if Sfx.sound_start:
            Sfx.sound_start.play()

    def pause():
        if Sfx.sound_pause:
            Sfx.sound_pause.play()

    def rotate():
        if Sfx.sound_rotate:
            Sfx.sound_rotate.play()

    def fall():
        if Sfx.sound_fall:
            Sfx.sound_fall.play()

    def landing():
        if Sfx.sound_landing:
            Sfx.sound_landing.play()

    def move():
        if Sfx.sound_move:
            Sfx.sound_move.play()

    def error():
        if Sfx.sound_error:
            Sfx.sound_error.play()

    def lines(n):
        if n == 1 and Sfx.sound_single:
            Sfx.sound_single.play()
        elif n == 2 and Sfx.sound_double:
            Sfx.sound_double.play()
        elif n == 3 and Sfx.sound_triple:
            Sfx.sound_triple.play()
        elif n == 4 and Sfx.sound_tetris:
            Sfx.sound_tetris.play()
