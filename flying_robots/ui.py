"""A basic curses interface for FlyingRobots."""

import curses

from .game import Game
from .exceptions import LevelComplete, GameOver
from .chars import gameclass
from .hs_handler import get_scores, add_score

def ctrl(ch):
    return chr(ord(ch)-96)

def unctrl(ch):
    return chr(ord(ch)+96) if is_ctrl(ch) else ch

def is_ctrl(ch):
    return 1 <= ord(ch) <= 26

class GameInterface:
    
    info_win_width = 18
    
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
    
    yn_vals = {
        'y':    True,
        'n':    False
        }
    
    def __init__(self, stdscr, config):
        self.stdscr = stdscr
        my, mx = stdscr.getmaxyx()      # size of screen
        gy = config['grid'].getint('y') + 2 # size required for grid
        gx = config['grid'].getint('x') + 2 + self.info_win_width
        if (my < gy) or (mx < gx):
            self.quit(1, 'flybots needs a screen of at least {}x{}.'.format(gx, gy))
        self.hiscore_game = config['game'].getboolean('hiscore')
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        self.stdscr.clear()
        self.game = Game(config)
        self.grid_size = self.game.grid_size
        self.setup_nonmove_cmds()
        self.setup_windows()
        self.update_grid()
        self.update_info()
        self.stdscr.refresh()
        self.mainloop()
    
    def setup_windows(self):
        x, y, _ = self.grid_size
        self.grid_win = self.stdscr.subwin(y+2, x+2, 0, 0)
        self.grid_win.border()
        self.info_win = self.stdscr.subwin(y+2, 18, 0, x+3)
        # Now get the positions where we'll indicate whether sticky mode,
        # move-as-far-as-possible mode etc, has been set.
        info_max_y, info_max_x = self.info_win.getmaxyx()
        self.sticky_yx = [info_max_y-2, 0]
        self.afap_yx = [info_max_y-2, 1]
    
    def setup_nonmove_cmds(self):
        """Here we bind keys to their functions."""
        self.nonmove_cmds = {
            'q':                    self.prompt_quit,
            chr(curses.KEY_NPAGE):  self.view_next_elev,
            chr(curses.KEY_PPAGE):  self.view_prev_elev,
            't':                    self.teleport,
            'p':                    self.zoom_to_player,
            'w':                    self.wait,
            'g':                    self.prompt_goto_elev,
            's':                    self.toggle_sticky_view,
            'f':                    self.toggle_afap
            }
    
    def play_again(self):
        self.game.start_game()
        self.update_grid()
        self.update_info()

    def update_grid(self):
        grid = self.game.view_grid()
        for row_num, row in enumerate(grid):
            chars = [self.charmap.get(gameclass(ch), ' ') for ch in row]
            self.grid_win.addstr(row_num+1, 1, ''.join(chars))
        self.grid_win.noutrefresh()
    
    def update_info(self):
        # Maybe make this less verbose
        x = 0
        self.info_win.erase()
        self.info_win.addstr(1, x, 'Player coords:')
        self.info_win.addstr(2, x, str(self.game.player_coords))
        self.info_win.addstr(4, x, 'Viewing elev:')
        self.info_win.addstr(5, x, str(self.game.elev))
        self.info_win.addstr(6, x, 'Level:')
        self.info_win.addstr(7, x, str(self.game.level))
        self.info_win.addstr(9, x, 'Enemies:')
        self.info_win.addstr(10, x, str(self.game.enemy_count))
        self.info_win.addstr(12, x, 'Score:')
        self.info_win.addstr(13, x, str(self.game.score))
        sticky = 's' if self.game.sticky_view else ' '
        y, x = self.sticky_yx
        self.info_win.addstr(y, x, sticky)
        afap = 'f' if self.game.move_afap else ' '
        y, x = self.afap_yx
        self.info_win.addstr(y, x, afap)
        self.info_win.noutrefresh()
    
    def mainloop(self):
        while True:
            x, y = self.game.player_coords[:2]
            cmd_key = chr(self.stdscr.getch(y+1, x+1))  # player posn on grid
            try:
                self.handle_cmd(cmd_key)
            except GameOver as e:
                self.on_game_over(*e.args)
            except LevelComplete:
                self.on_level_complete()
            self.stdscr.refresh()

    def handle_cmd(self, cmd):
        if unctrl(cmd).lower() in self.xy_move_keys:
            self.move(cmd)
        elif cmd in self.nonmove_cmds:
            self.nonmove_cmds[cmd]()
        self.update_info()
    
    def move(self, cmd):
        if is_ctrl(cmd):
            z = -1
        elif cmd.isupper():
            z = 1
        else:
            z = 0
        x, y = self.xy_move_keys[unctrl(cmd).lower()]
        self.game.move_player(x, y, z)
        self.update_grid()
    
    def teleport(self):
        self.game.teleport_player()
        self.update_grid()
    
    def zoom_to_player(self):
        self.game.zoom_to_player()
        self.update_grid()
    
    def view_elev(self, elev):
        if 0 <= elev < self.grid_size[2]:
            self.game.elev = elev
            self.update_grid()
    
    def view_next_elev(self):
        self.view_elev(self.game.elev-1)
    
    def view_prev_elev(self):
        self.view_elev(self.game.elev+1)
    
    def wait(self):
        self.game.wait()
    
    def get_yn(self, prompt, default=True, prompt_coords=[0, 0]):
        y, x = prompt_coords
        self.grid_win.addstr(y, x, prompt)
        ch = chr(self.grid_win.getch(y, x)).lower()
        self.grid_win.border()
        self.grid_win.refresh()
        return self.yn_vals.get(ch, default)
    
    def get_num(self, prompt, default=None):
        self.grid_win.addstr(0, 0, prompt)
        try:
            curses.echo()
            val = int(self.grid_win.getstr(0, len(prompt)))
        except ValueError:
            val = default
        curses.noecho()
        self.grid_win.border()
        self.grid_win.refresh()
        return val
    
    def on_level_complete(self):
        self.game.next_level()
        self.update_grid()
        self.update_info()

    def on_game_over(self, victory, msg=None):
        if msg is None:
            msg = "You win!" if victory else "You lose!"
        self.grid_win.addstr(0, 0, msg)
        play_again = self.get_yn('Play again? (y/N)', default=False, prompt_coords=[1, 0])
        # If this was a hiscore game, store the player's scores.
        # If player doesn't want to play another game, print the high scores.
        store_hs = self.hiscore_game
        print_hs = not play_again
        self.handle_hiscores(store_hs, print_hs)
        if play_again:
            self.play_again()
        else:
            self.quit()
    
    def prompt_quit(self):
        if self.get_yn('Really quit? (y/N)', False):
            self.quit()
    
    def prompt_goto_elev(self):
        elev = self.get_num('Goto: ', self.game.elev)
        if 0 < elev <= self.grid_size[2]:
            self.game.zoom_to_elev(elev)
        self.update_grid()
    
    def toggle_sticky_view(self):
        self.game.toggle_sticky_view()
        self.update_info()
    
    def toggle_afap(self):
        self.game.toggle_afap()
        self.update_info()
    
    def handle_hiscores(self, store, prnt):
        if store:
            scores, posn = add_score(self.game.name, self.game.score)
        else:
            scores, posn = get_scores(), None
        if prnt:
            self.print_hiscores(scores, posn)
    
    def print_hiscores(self, scores, posn):
        self.grid_win.clear()
        self.grid_win.addstr(1, 1, 'Pos\tName\tScore')
        for _posn, (name, score) in enumerate(scores):
            line = _posn+2
            _posn += 1   # Because position in score list starts from 1, not 0.
            if _posn == posn:
                attr = curses.A_STANDOUT
            else:
                attr = curses.A_NORMAL
            self.grid_win.addstr(line, 1, '{}\t{}\t{}'.format(_posn, name, score), attr)
        self.grid_win.refresh()
        self.stdscr.getch(0, 0) # Wait until player hits a key before quitting.

    def quit(self, status=0, msg=None):
        self.stdscr.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        if msg is not None:
            print(msg)
        quit(status)
