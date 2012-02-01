class BadCharmapError(BaseException): pass

from debug import log
from exceptions import BadTileError

gameclasses = {
        'empty',
        'junk',
        'robot',
        'player'
        }

def is_valid_charmap(charmap):
    # Currently, this just checks if all members of gameclasses are in charmap.
    # We should probably warn non-fatally if charmap has keys not in gameclasses.
    implemented_chars = set(charmap.keys())
    return implemented_chars.issuperset(gameclasses)

def gameclass(obj):
    if obj is None:
        return 'empty'
    else:
        return obj.CLASS

class BaseObject:
    
    """A base class representing anything that can occupy a tile on a
    grid."""
    
    CLASS = ''
    
    def __init__(self, coords, grid):
        self.coords = coords
        self._grid = grid

class Junk(BaseObject):
    
    """A class representing the junk left behind when 2 or more robots
    collide."""
    
    CLASS = 'junk'

class BaseMoveableObject(BaseObject):
    
    """A base class representing anything that can move on a grid."""

    def _move_to(self, new_coords):
        if self.CLASS == 'player':
            log('moving to {}'.format(new_coords))
        # Following code raises BadTileError is tile is OOB, halting move.
        self._grid._set_tile(new_coords, self)
  

    def _move_by(self, dx, dy, dz):
        """Arguments are changes in x, y, z coords respectively."""
        old = self.coords
        new = [old[0] + dx, old[1] + dy, old[2] + dz]
        self._move_to(new)

class BaseEnemy(BaseMoveableObject):
    
    CLASS = None
    KILLSCORE = None
    
    def __init__(self, coords, grid, speed=1):
        self.is_alive = True
        BaseMoveableObject.__init__(self, coords, grid)

class Robot(BaseMoveableObject):
    
    CLASS = 'robot'
    KILLSCORE = 10

    def __init__(self, coords, grid, speed=1):
        self._speed = speed
        BaseEnemy.__init__(self, coords, grid)
    
    def _move_towards_player(self):
        to_move = []
        self_coords = self.coords
        player_coords = self._grid.player.coords
        for s, p in zip(self_coords, player_coords):
            if s < p:
                to_move.append(1)
            elif s > p:
                to_move.append(-1)
            else:
                to_move.append(0)
        self._move_by(*to_move)
    
    def move(self):
        for _ in range(self._speed):
            self._move_towards_player()

class TestRobot(Robot):
    """An enemy that doesn't move, for testing purposes."""
    
    CLASS = 'robot'
    KILLSCORE = 10
    
    def move(self):
        pass

class Player(BaseMoveableObject):
    
    CLASS = 'player'
    
    def _move_by(self, dx, dy, dz):
        # Players have a special version of _move_by that first checks if
        # the tile is empty.
        old = self.coords
        new = [old[0] + dx, old[1] + dy, old[2] + dz]
        if not self._grid._tile_is_empty(new):
            raise BadTileError('Player cannot move onto occupied tile.')
        self._move_to(new)
    
    def move(self, dx, dy, dz):
        self._move_by(dx, dy, dz)
    
    def teleport(self):
        new = self._grid._get_random_empty_coords()
        self._move_to(new)
