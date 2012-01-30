from game import Game
from ui import GameInterface

# Forget all this stuff about command parsing; go back to normal UI wrapping
# around the game and calling its functions.

game_cmds = {
        'move',
        'wait',
        'tele',
        'quit'
        }

def get_cmd_funcs(cmd_dict=None, **kwargs):
    """Takes a dictionary mapping game commands to functions, or a
    series of keyword arguments in the form cmd=func.
    Verifies that all the necessary game commands are implemented,
    and returns a dict mapping game commands to functions."""
    if cmd_dict is not None:
        _dict = cmd_dict
    else:
        _dict = kwargs
    implemented_cmds = set(_dict.keys())
    if not implemented_cmds.issuperset(game_cmds):
        raise CommandsNotImplemented(game_cmds.difference(implemented_cmds))
    else:
        return _dict

class Main:

    """The main purpose of this class is to tie together the actual game logic
    in GameGrid and the user interface in GameInterface."""

    def __init__(self):
        self.game = Game()
        self.setup_ui()

    def setup_ui(self)
        try:
            self._ui = GameInterface(def_x, def_y)
        except UIError as e:
            raise e
  
    def draw_grid(self):
        self._ui.draw_grid(self.game.view_grid(self.current_elev))

    def draw_score(self):
        self._ui.draw_score(self.game.score)
    
    def draw_level_num(self):
        self._ui.draw_level_num(self.game.level)
    
    def draw_all(self):
        self.draw_grid()
        self.draw_score()
        self.draw_level_num()
    
    def view_elev(self, elev):
        self.current_elev = elev
        self.draw_grid()
    
    def view_next_elev(self):
        self.view_elev(self.current_elev+1)
    
    def view_prev_elev(self):
        self.view_elev(self.current_elev-1)
    
    def view_player_elev(self):
        self.view_elev(self.player.coords[2])

    def turn(self):
        self.player.move(*self._interface.get_player_move())
        self._grid.move_enemies()

    def mainloop(self):
        while True:
            try:
                self.turn()
                self.draw_grid()
                self.draw_score()
            except LevelComplete:
                self.level_complete()
            except GameOver:
                self.game_over()

    def parse_cmd(self, cmd):
        tokens = cmd.split()
        cmd = tokens.pop(0)
        if cmd == 'move':
            self.game.move_player(*[int(i) for i in tokens])
        elif cmd == 'view':
            elev = tokens[0]
            if elev == 'player':
                self.view_player_elev()
            elif elev == 'up':
                self.view_next_elev()
            elif elev == 'down':
                self.view_prev_elev()
        elif cmd == 'quit':
            self.quit()
            

    def mainloop(self):
        while True:
            cmd = self._ui.get_input()

    def level_complete(self):
        self.game.next_level()
        self.draw_all()

    def game_over(self):
        self._ui.game_over(self.game.level, self.game.score)
        quit()

    def quit(self):
        self._ui.close()
        quit()
