from chars import gameclass
from grid import GameGrid
from exceptions import BadTileError, LevelComplete, GameOver
from config import get_config

def calc_enemies(level):
    # This is very primitive, for testing purposes.
    # TODO: make this more sophisticated, and able to handle an
    # arbitrary number of levels.
    # An idea is to take whatever bsd-robots has ** (3/2).
    return 40 * level

class Game:

    def __init__(self, config=None, start_level=1):
        config = config or get_config()
        self.level = start_level
        self.score = 0
        x = config['size'].getint('x')
        y = config['size'].getint('y')
        z = config['size'].getint('z')
        self.grid_size = [x, y, z]
        self._grid = GameGrid(x, y, z, self)
        #self._grid.populate(calc_enemies(start_level))
        self._grid.populate_test(calc_enemies(start_level))
        self.player = self._grid.player
        self.elev = self.player.coords[2]
        self.zoom_to_player_on_move = config['view'].getboolean('zoom_to_player_on_move')
        self.zoom_to_player_on_tele = config['view'].getboolean('zoom_to_player_on_teleport')
    
    # The following are functions called by the UI to change game state
    
    def teleport_player(self):
        self.player.teleport()
        if self.zoom_to_player_on_tele:
            self.zoom_to_player()
    
    def move_player(self, dx, dy, dz):
        try:
            self.player.move(dx, dy, dz)
        except BadTileError:
            return False
        self._grid.move_enemies()
        if self.zoom_to_player_on_move:
            self.zoom_to_player()
        return True
    
    def next_level(self):
        self.level += 1
        self._grid.populate(self.level)
    
    def zoom_to_player(self):
        self.elev = self.player.coords[2]
    
    
    # The following are functions called by the UI in order to display the
    # game to the player.
    
    def view_grid(self):
        return self._grid.view_plan(self.elev)
    
    @property
    def enemy_count(self):
        return len(self._grid._enemies)
