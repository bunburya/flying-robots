from chars import gameclass
from grid import GameGrid
from exceptions import BadTileError, LevelComplete, GameOver
from config import get_config
from debug import log

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
        self._grid.populate(calc_enemies(start_level))
        self.elev = self._grid.player.coords[2]
        self.zoom_to_player_on_move = config['view'].getboolean('zoom_to_player_on_move')
        self.zoom_to_player_on_tele = config['view'].getboolean('zoom_to_player_on_teleport')
    
    # The following are functions called by the UI to change game state
    
    def teleport_player(self):
        self._grid.player.teleport()
        self._grid.set_tile(self._grid.player)
        if self.zoom_to_player_on_tele:
            self.zoom_to_player()
    
    def move_player(self, dx, dy, dz):
        try:
            self._grid.player.move(dx, dy, dz)
        except BadTileError:
            return False
        self._grid.set_tile(self._grid.player)
        self._grid.move_enemies()
        if self.zoom_to_player_on_move:
            self.zoom_to_player()
        return True
    
    def next_level(self):
        log('next level.')
        self.level += 1
        self._grid.populate(calc_enemies(self.level))
        self.zoom_to_player()
    
    def zoom_to_player(self):
        self.elev = self._grid.player.coords[2]
    
    
    # The following are functions called by the UI in order to display the
    # game to the player.
    
    def view_grid(self):
        return self._grid.view_plan(self.elev)
    
    @property
    def player_coords(self):
        return self._grid.player.coords
    
    @property
    def enemy_count(self):
        return len(self._grid._enemies)
