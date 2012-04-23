"""A graphical user interface for FlyingRobots, using Tkinter."""

from os.path import join, dirname

import tkinter
from tkinter import N, W, E, S
from tkinter.messagebox import askquestion, showinfo
from tkinter.simpledialog import askinteger

from ..game import Game
from ..exceptions import LevelComplete, GameOver
from ..chars import gameclass
from ..hs_handler import get_scores, add_score
from ..metadata import long_name, version

from ._common import charmap, xy_move_keys

GFX_DIR = join(dirname(__file__), 'gfx')

img_w, img_h = 10, 20

charmap = {
        'player':   join(GFX_DIR, 'player.gif'),
        'robot':    join(GFX_DIR, 'robot.gif'),
        'junk':     join(GFX_DIR, 'junk.gif')
        }


class GameInterface(tkinter.Frame):
    
    xy_move_keys = xy_move_keys

    yn_vals = {
            'yes':  True,
            'no':   False
            }
    
    def __init__(self, config, master=None):
        tkinter.Frame.__init__(self, master)
        self.hiscore_game = config['game'].getboolean('hiscore')
        self.gen_charmap()
        self.game_over = False
        self.game = Game(config)
        self.grid_size = self.game.grid_size
        w, h, _ = self.grid_size
        self.grid_imgs = set()
        self.grid_widget_h = h * img_h
        self.grid_widget_w = w * img_w
        self.grid()
        self.setup_nonmove_cmds()
        self.bind_all('<Any-KeyPress>', self.handle_keypress)
        self.setup_widgets()
        self.update_grid()
        self.update_info()

    def gen_charmap(self):
        _charmap = {}
        for char in charmap:
            _charmap[char] = tkinter.PhotoImage(file=charmap[char])
        self.charmap = _charmap

    def setup_widgets(self):

        # TODO:
        # - Insert blank Labels between lines to space out the info.
        x, y, z = self.grid_size

        self.grid_widget = tkinter.Canvas(
                self,
                height=self.grid_widget_h,
                width=self.grid_widget_w
                )

        # A Frame to hold all the non-grid widgets
        info_frame = tkinter.Frame(self)

        ## Labels for displaying other game data
        coords_frame = tkinter.Frame(info_frame)
        coords_head = tkinter.Label(
                coords_frame,
                text='Player coords:'
                )
        self.coords_var = tkinter.StringVar()
        coords_label = tkinter.Label(
                coords_frame,
                textvariable=self.coords_var
                )
        coords_head.grid(sticky=N+W)
        coords_label.grid(row=0, column=1, sticky=N+W)
        
        ## Spinbox controlling elevation currently being viewed,
        ## and button to zoom to player
        elev_frame = tkinter.Frame(info_frame)
        self.elev_var = tkinter.StringVar()
        elev_label = tkinter.Label(
                elev_frame,
                text='Elev:'
                )
        elev_spinbox = tkinter.Spinbox(
                elev_frame,
                command=self.view_elev,
                from_=0,
                to=(z-1),
                increment=1,
                textvariable=self.elev_var,
                width=2,
                state='readonly'
                )
        view_player_button = tkinter.Button(
                elev_frame,
                anchor=tkinter.CENTER,
                command=self.view_player_elev,
                height=1,
                text='player'
                )
        elev_label.grid(sticky=N+W)
        elev_spinbox.grid(row=0, column=1, sticky=N+W)
        view_player_button.grid(row=0, column=2, sticky=N+W)

        ## Label containing current game level.
        level_frame = tkinter.Frame(info_frame)
        level_head = tkinter.Label(
                level_frame,
                text='Level:'
                )
        self.level_var = tkinter.StringVar()
        level_label = tkinter.Label(
                level_frame,
                textvariable=self.level_var
                )
        level_head.grid(sticky=N+W)
        level_label.grid(row=0, column=1, sticky=N+W)

        ## Label containing current enemy count.
        enemies_frame = tkinter.Frame(info_frame)
        enemies_head = tkinter.Label(
                enemies_frame,
                text='Enemies:'
                )
        self.enemies_var = tkinter.StringVar()
        enemies_label = tkinter.Label(
                enemies_frame,
                textvariable=self.enemies_var
                )
        enemies_head.grid(sticky=N+W)
        enemies_label.grid(row=0, column=1, sticky=N+W)

        ## Label containing current score.
        score_frame = tkinter.Frame(info_frame)
        score_head = tkinter.Label(
                score_frame,
                text='Score:'
                )
        self.score_var = tkinter.StringVar()
        score_label = tkinter.Label(
                score_frame,
                textvariable=self.score_var
                )
        score_head.grid(sticky=N+W)
        score_label.grid(row=0, column=1, sticky=N+W)

        ## Checkbuttons for sticky and AFAP modes
        modes_frame = tkinter.Frame(info_frame)
        self.sticky_var = tkinter.IntVar()
        sticky_chbox = tkinter.Checkbutton(
                modes_frame,
                command=self.toggle_sticky,
                text='Sticky mode',
                variable=self.sticky_var
                )
        self.afap_var = tkinter.IntVar()
        afap_chbox = tkinter.Checkbutton(
                modes_frame,
                command=self.toggle_afap,
                text='Move as far as possible',
                variable=self.afap_var
                )
        sticky_chbox.grid(sticky=N+W)
        afap_chbox.grid(row=1, sticky=N+W)

        # Now call .grid() on each widget to paint it to the screen
        self.grid_widget.grid(sticky=N+E+S+W)
        coords_frame.grid(sticky=N+W)
        elev_frame.grid(sticky=N+W)
        level_frame.grid(sticky=N+W)
        enemies_frame.grid(sticky=N+W)
        score_frame.grid(sticky=N+W)
        modes_frame.grid(sticky=N+W)

        info_frame.grid(row=0, column=1, sticky=N+E+S+W)

    def update_grid(self):
        obj_grid = self.game.view_grid()
        self.grid_widget.delete(tkinter.ALL)
        for obj in self.game.objects:
            x, y, z = obj.coords
            if not z == self.game.elev:
                continue
            x_pos = x * img_w
            y_pos = y * img_h
            self.grid_imgs.add(
                    self.grid_widget.create_image(x_pos, y_pos, 
                        image=self.charmap[gameclass(obj)],
                        anchor=tkinter.NW)
                    )

    def view_elev(self, elev=None):
        if elev is None:
            elev = int(self.elev_var.get())
        if 0 <= elev < self.grid_size[2]:
            self.elev_var.set(elev)
            self.game.elev = elev
            self.update_grid()

    def view_next_elev(self):
        elev = int(self.elev_var.get()) + 1
        self.view_elev(int(self.elev_var.get())+1)

    def view_prev_elev(self):
        self.view_elev(int(self.elev_var.get())-1)

    def view_player_elev(self):
        self.view_elev(self.game.player_coords[2])

    def toggle_sticky(self):
        self.game.toggle_sticky_view()
        self.sticky_var.set(self.game.sticky_view)

    def toggle_afap(self):
        self.game.toggle_afap()
        self.afap_var.set(self.game.move_afap)

    def setup_nonmove_cmds(self):
        self.nonmove_cmds = {
                'q':        self.prompt_quit,
                'Prior':    self.view_next_elev,
                'Next':     self.view_prev_elev,
                't':        self.teleport,
                'p':        self.view_player_elev,
                'w':        self.wait,
                'g':        self.prompt_goto_elev,
                's':        self.toggle_sticky,
                'f':        self.toggle_afap
                }

    def move(self, event):
        """Takes an Event instance which represents a movement key,
        and processes movement accordingly.
        """
        x, y = self.xy_move_keys[event.keysym.lower()]
        if (event.state & 1) or (event.state & 2):  # Shift or caps lock
            z = 1
        elif event.state & 4:   # Ctrl key
            z = -1
        else:
            z = 0
        self.game.move_player(x, y, z)
        self.update_grid()
        self.update_info()

    def teleport(self):
        self.game.teleport_player()
        self.update_grid()
        self.update_info()

    def handle_keypress(self, event):
        if self.game_over:
            return
        key = event.keysym
        try:
            if key.lower() in self.xy_move_keys:
                self.move(event)
            elif key in self.nonmove_cmds:
                self.nonmove_cmds[key]()
        except LevelComplete:
            self.on_level_complete()
        except GameOver as e:
            self.on_game_over(*e.args)

    def on_level_complete(self):
        self.game.next_level()
        self.update_grid()
        self.update_info()

    def on_game_over(self, victory, msg=None):
        self.game_over = True
        if msg is None:
            msg = 'You win!' if victory else 'You lose!'
        play_again = self.get_yn('{}\nPlay again?'.format(msg))
        store_hs = self.hiscore_game
        print_hs = not play_again
        self.handle_hiscores(store_hs, print_hs)
        if play_again:
            self.play_again()
        else:
            self.quit()

    def play_again(self):
        self.game_over = False
        self.game.start_game()
        self.update_grid()
        self.update_info()

    def handle_hiscores(self, store, _print):
        if store:
            scores, posn = add_score(self.game.name, self.game.score)
        else:
            scores, posn = get_scores(), None
        if _print:
            self.print_hiscores(scores, posn)

    def print_hiscores(self, scores, posn):
        to_print = []
        for _posn, (name, score) in enumerate(scores):
            _posn += 1
            if _posn == posn:
                to_print.append('*{}\t{}\t{}'.format(_posn, name, score))
            else:
                to_print.append('{}\t{}\t{}'.format(_posn, name, score))
        showinfo(title='High scores', message='\n'.join(to_print))

    def get_yn(self, msg):
        return self.yn_vals[askquestion(message=msg)]

    def update_info(self):
        """Get game state and copy it into control variables."""
        self.coords_var.set(self.game.player_coords)
        self.elev_var.set(self.game.elev)
        self.level_var.set(self.game.level)
        self.enemies_var.set(self.game.enemy_count)
        self.score_var.set(self.game.score)
        self.sticky_var.set(self.game.sticky_view)
        self.afap_var.set(self.game.move_afap)

    def prompt_quit(self):
        if self.get_yn('Really quit?'):
            self.quit()

    def wait(self):
        self.game.wait()

    def prompt_goto_elev(self):
        self.view_elev(askinteger('', 'Goto:'))

def start_interface(config):
    root = tkinter.Tk()
    root.title('{} v{}'.format(long_name, version))
    ui = GameInterface(config, root)
    ui.mainloop()
