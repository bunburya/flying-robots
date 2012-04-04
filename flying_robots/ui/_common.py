"""This module holds data and functions common to both interfaces
(curses and tkinter). The contents of this module are subject to change."""

charmap = {
    'robot':    '+',
    'player':   '@',
    'empty':    ' ',
    'junk':     '*'
    }
    
xy_move_keys = {
    'h':    (-1, 0),
    'j':    (0, 1),
    'k':    (0, -1),
    'l':    (1, 0),
    'b':    (-1, 1),
    'n':    (1, 1),
    'y':    (-1, -1),
    'u':    (1, -1),
    'x':    (0, 0)
    }
