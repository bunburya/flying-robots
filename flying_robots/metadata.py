long_name = 'FlyingRobots'
short_name = 'flybots'
version = '0.4.0'
description = 'A three-dimensional clone of the classic bsd-robots game.'
author = 'Alan Bunbury'
homepage_url = 'http://bunburya.github.com/FlyingRobots'
download_url = 'https://github.com/bunburya/FlyingRobots'
license = 'MIT'
controls = """CONTROLS

Basic movement buttons are:

y k u
 \|/
h-x-l
 /|\\
b j n

Holding shift while pressing any of the above also moves up the z-axis.
Holding ctrl while pressing any of the above also moves down the z-axis.

t = Teleport to random location.
w = Stay where you are and pass turns until you complete the level or die.
    You get a 10% bonus to score for each robot who dies in this period,
    but it only counts if you complete the level.
s = Toggle "sticky" mode, in which your view stays fixed on the current
    elevation even when you move. In the curses interface, sticky mode is
    indicated by the presence of an "s" at the bottom of the info pane.
f = Toggle "as-far-as-possible" mode. When you press a movement key while in
    this mode, you move as far as is safe in that direction. In the curses
    interface, as-far-as-possible mode is indicated by the presence of a "f"
    at the bottom of the info pane.
    This mode is unset after each turn.
q = Quit.

Pg-up = View next level on z-axis, without moving.
Pg-dn = View previous level on z-axis, without moving.
p = View level on z-axis on which player is placed, without moving.
g = Prompt for number of level on z-axis and view that level, without moving.
"""
