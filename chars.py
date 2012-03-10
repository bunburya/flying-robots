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
        self._grid.clear_tile(self.coords)
        self.coords = new_coords

    def _move_by(self, dx, dy, dz, empty_only=False, safe_only=False):
        """Arguments are changes in x, y, z coords respectively.
        If optional fourth empty_only arg is True, raises BadTileError if
        tile being moved to is occupied. This is used when the player moves."""
        stay = (dx == dy == dz == 0)
        old = self.coords
        new = [old[0] + dx, old[1] + dy, old[2] + dz]
        # TODO: Get rid of BadTileError, and just return without doing anything
        # instead.
        # Possibly return a bool, okay_to_proceed, indicating whether the move
        # was successful.
        if not self._grid.is_valid_tile(new):
            raise BadTileError('Tile out of bounds.')
        if empty_only and (not stay) and (not self._grid._tile_is_empty(new)):
            raise BadTileError('Player cannot move onto occupied tile.')
        if safe_only and (not self._grid.tile_is_safe(new)):
            raise BadTileError('Tile not safe.')
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
    
    def _move_towards_player(self, times=1):
        to_move = []
        self_coords = self.coords
        player_coords = self._grid.player.coords
        for s, p in zip(self_coords, player_coords):
            if s < p:
                to_move.append(times)
            elif s > p:
                to_move.append(-times)
            else:
                to_move.append(0)
        self._move_by(*to_move)
    
    def move(self):
        self._move_towards_player(self._speed)

class Player(BaseMoveableObject):
    
    CLASS = 'player'
    
    def move(self, dx, dy, dz, safe_only=False):
        self._move_by(dx, dy, dz, True, safe_only)
    
    def teleport(self):
        new = self._grid._get_random_empty_coords()
        self._move_to(new)
