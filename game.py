from chars import gameclass
from grid import GameGrid
from exceptions import BadTileError, LevelComplete, GameOver
from config import get_config, calc_enemies
from debug import log

class Game:

    def __init__(self, config):
        self.level = config['game'].getint('start_level')
        self.score = 0
        self.waiting = False
        self.wait_bonus = 0
        x = config['grid'].getint('x')
        y = config['grid'].getint('y')
        z = config['grid'].getint('z')
        self.name = config['player']['name']
        self.grid_size = [x, y, z]
        self.grid = GameGrid(x, y, z, self)
        self.grid.populate(calc_enemies(self.level))
        self.elev = self.grid.player.coords[2]
        self.sticky_view = False
        self.move_afap = False
    
    # The following are functions called by the UI to change game state
    
    def teleport_player(self):
        self.grid.player.teleport()
        self.grid.place_char(self.grid.player)
        self.grid.move_enemies()
        if not self.sticky_view:
            self.zoom_to_player()
    
    def move_player(self, dx, dy, dz, safe_only=True):
        # This isn't absolutely ideal, but it allows for the player to move
        # as far as possible in the given direction if self.move_afap=True.
        afap = self.move_afap
        move_it = True
        while move_it:
            try:
                self.grid.player.move(dx, dy, dz, safe_only)
            except BadTileError:
                break
            self.grid.place_char(self.grid.player)
            self.grid.move_enemies()
            if not self.sticky_view:
                self.zoom_to_player()
            move_it = afap
        self.move_afap = False
    
    def wait(self):
        self.waiting = True
        while True:
            self.move_player(0, 0, 0, False)
    
    def next_level(self):
        log('next level.')
        self.waiting = False
        self.move_afap = False
        self.sticky_view = False
        self.score += self.wait_bonus
        self.wait_bonus = 0
        self.level += 1
        self.grid.populate(calc_enemies(self.level))
        self.zoom_to_player()
    
    def zoom_to_player(self):
        self.elev = self.grid.player.coords[2]
    
    def zoom_to_elev(self, elev):
        self.elev = elev
    
    def toggle_sticky_view(self):
        self.sticky_view = not self.sticky_view
    
    def toggle_afap_view(self):
        self.move_afap = not self.move_afap
    
    # The following are functions called by the UI in order to display the
    # game to the player.
    
    def view_grid(self):
        return self.grid.view_plan(self.elev)
    
    @property
    def player_coords(self):
        return self.grid.player.coords
    
    @property
    def enemy_count(self):
        return len(self.grid.enemies)
