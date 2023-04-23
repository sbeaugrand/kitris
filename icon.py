#!/usr/bin/env python3
# ---------------------------------------------------------------------------- #
## \file icon.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
import sys
import svgwrite
from math import *
from shape import Shape
from colors import Colors

w = 9
h = 9
d = svgwrite.Drawing(sys.argv[1], (800, 800 * h / w))
d.viewbox(0, -h, w, h)


def draw_block(x, y, color):
    c = Colors.color1(color)
    c1 = '#{:02x}{:02x}{:02x}'.format(int(c[0] * 255), int(c[1] * 255),
                                      int(c[2] * 255))
    c = Colors.color2(color)
    c2 = '#{:02x}{:02x}{:02x}'.format(int(c[0] * 255), int(c[1] * 255),
                                      int(c[2] * 255))
    c = Colors.color3(color)
    c3 = '#{:02x}{:02x}{:02x}'.format(int(c[0] * 255), int(c[1] * 255),
                                      int(c[2] * 255))
    d.add(d.rect(insert=(x, -y), fill=c1))
    e = 1 / 24
    e2 = e / 2
    d.add(
        d.polyline(points=[(x + e, -(y - 1 + e2)), (x + 1 - e2, -(y - 1 + e2)),
                           (x + 1 - e2, -(y - e))],
                   fill='none',
                   stroke=c2,
                   stroke_width=e))
    d.add(
        d.polyline(points=[(x + e * 2, -(y - 1 + e2 * 3)),
                           (x + 1 - e, -(y - 1 + e2 * 3)),
                           (x + 1 - e, -(y - e * 2))],
                   fill='none',
                   stroke=c2,
                   stroke_width=e))
    d.add(
        d.polyline(points=[(x + 1 - e, -(y - e2)), (x + e2, -(y - e2)),
                           (x + e2, -(y - 1 + e2 * 2))],
                   fill='none',
                   stroke=c3,
                   stroke_width=e))
    d.add(
        d.polyline(points=[(x + 1 - e * 2, -(y - e2 * 3)),
                           (x + e, -(y - e2 * 3)),
                           (x + e2 * 3, -(y - 1 + e * 2))],
                   fill='none',
                   stroke=c3,
                   stroke_width=e))


def draw_shape(n, x, y, r):
    path = Shape(1, n).path()
    draw_block(x, y, n)
    for i in range(0, 6, 2):
        if r == 0:
            draw_block(x + path[i], y + path[i + 1], n)
        elif r == 1:
            draw_block(x - path[i + 1], y + path[i], n)
        elif r == 2:
            draw_block(x - path[i], y - path[i + 1], n)
        elif r == 3:
            draw_block(x + path[i + 1], y - path[i], n)


d.add(d.rect(insert=(0, -h), size=(w, h), fill='black', rx=1))
draw_shape(2, 2, 7, 3)
draw_shape(0, 4, 7, 0)
draw_shape(2, 6, 7, 2)
draw_shape(6, 1, 3, 0)
draw_shape(0, 4, 2, 0)
draw_shape(5, 7, 3, 0)
for i in range(0, 9):
    draw_block(i, 5, 7)
d.save()
