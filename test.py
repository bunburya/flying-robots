#!/usr/bin/env python3

from chars import *
from grid import *

charmap = {
        'player': '@',
        'junk': '*',
        'robot': '+',
        'empty': ' '
        }

assert is_valid_charmap(charmap)

g = GameGrid(20, 20, 20, 50)
for elev in range(20):
    p = g.view_plan(charmap=charmap, elev=elev)
    print('Level {}'.format(elev))
    for row in p:
        print(''.join(row))
