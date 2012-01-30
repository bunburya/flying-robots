"""A basic curses interface for FlyingRobots."""

import curses

# def_x and def_y are default grid width and height; eventually,
# we should get these from a config file.
from game import Game, LevelComplete, GameOver
from chars import gameclass

def ctrl(ch):
    return chr(ord(ch)-96)

def unctrl(ch):
    return chr(ord(ch)+96) if is_ctrl(ch) else ch

def is_ctrl(ch):
    return 1 >= ord(ch) >= 26

class GameInterface:
    
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
        'u':    (1, -1)
        }
    
    yn_vals = {
        'y':    True,
        'n':    False
        }
    
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        self.stdscr.clear()
        self.game = Game()
        self.grid_size = self.game.grid_size
        self.setup_nonmove_cmds()
        self.setup_windows()
        self.update_grid()
        self.stdscr.refresh()
        self.mainloop()
    
    def setup_windows(self):
        x, y, _ = self.grid_size
        self.grid_win = self.stdscr.subwin(y+2, x+2, 0, 0)
        self.grid_win.border()
        # Also add in info grid.
    
    def setup_nonmove_cmds(self):
        """Here we bind keys to their functions."""
        self.nonmove_cmds = {
            'q':                    self.prompt_quit,
            chr(curses.KEY_NPAGE):  self.view_next_elev,
            chr(curses.KEY_PPAGE):  self.view_prev_elev,
            't':                    self.teleport,
            'p':                    self.zoom_to_player
            }
    
    def update_grid(self):
        grid = self.game.view_grid()
        for row_num, row in enumerate(grid):
            chars = [self.charmap.get(gameclass(ch), ' ') for ch in row]
            self.grid_win.addstr(row_num+1, 1, ''.join(chars))
        self.grid_win.noutrefresh()
    
    def mainloop(self):
        while True:
            y, x = reversed(self.game.player.coords[:2])
            cmd_key = chr(self.stdscr.getch(0, 0))
            self.handle_cmd(cmd_key)
            self.stdscr.refresh()

    def handle_cmd(self, cmd):
        if unctrl(cmd) in self.xy_move_keys:
            self.move(cmd)
        elif cmd in self.nonmove_cmds:
            self.nonmove_cmds[cmd]()
    
    def move(self, cmd):
        if is_ctrl(cmd):
            z = -1
        elif cmd.isupper():
            z = 1
        else:
            z = 0
        x, y = self.xy_move_keys[unctrl(cmd)]
        try:
            self.game.move_player(x, y, z)
        except GameOver:
            self.on_game_over()
        except LevelComplete:
            self.on_level_complete()
        self.update_grid()
    
    def teleport(self):
        self.game.teleport_player()
        self.update_grid()
    
    def zoom_to_player(self):
        self.game.zoom_to_player()
    
    def view_elev(self, elev):
        if elev in range(self.grid_size[1]):
            self.game.elev = elev
            self.update_grid()
    
    def view_next_elev(self):
        self.view_elev(self.game.elev+1)
    
    def view_prev_elev(self):
        self.view_elev(self.game.elev-1)
    
    def get_yn(self, prompt, default=True):
        prev = self.grid_win.instr(0, 0, len(prompt))
        self.grid_win.addstr(0, 0, prompt)
        ch = chr(self.grid_win.getch(1, 0)).lower()
        return self.yn_vals.get(ch, default)
    
    def on_level_complete(self):
        self.game.next_level()
        self.update_grid()

    def on_game_over(self):
        self.quit()
    
    def prompt_quit(self):
        if self.get_yn('Really quit? (y/N)', False):
            self.quit()

    def quit(self, status=0):
        self.stdscr.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        quit(status)
