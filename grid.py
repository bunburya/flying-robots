import random
from copy import deepcopy

from chars import Player, Robot, TestRobot, Junk, gameclass
from exceptions import BadTileError, LevelComplete, GameOver

from debug import log

class BaseGrid:
    
    """A base 3D grid.
    
    The z-axis represents the vertical depth of the grid. The x and y
    axes refer to the columns and rows, respectively, of each z-level
    when viewed from above.
    
    The origin (0, 0, 0) should be at the bottom-left corner of the
    plan and the top-left corner of the elevation."""

    
    def __init__(self, x, y, z):
        self._EMPTY_GRID = self._get_empty_grid(x, y, z)
        self._EMPTY_PLAN = self._get_empty_view(x, y)
        self._EMPTY_ELEV = self._get_empty_view(x, z)
        self._grid = self._copy_empty_grid()
        self.x = x
        self.y = y
        self.z = z
    
    def _get_empty_grid(self, x, y, z):
        """Creates an empty grid of the appropriate dimensions and
        binds it to the current instance."""
        return [[[None for i in range(x)] for j in range(y)] for k in range(z)]
    
    def _get_empty_view(self, x, y):
        """Creates an empty 2D grid, representing a view of the 3D grid."""
        return [[None for i in range(x)] for j in range(y)]

    def _copy_empty_grid(self):
        """Returns a deepcopy of the instance's empty grid; this is more
        efficient than generating a new one from scratch every time."""
        return [x[:] for x in [y[:] for y in [z[:] for z in self._EMPTY_GRID]]]
    
    def _copy_empty_view(self, view):
        return [x[:] for x in [y[:] for y in view]]
    
    def _set_tile(self, coords, new=None):
        x, y, z = coords
        if new is not None:
            incumbent = self._get_tile(coords)
            new_class = gameclass(new)
            incumbent_class = gameclass(incumbent)
            if incumbent_class != 'empty' and new_class != 'junk':
                # Moveable object is being moved onto a tile where another
                # object already stands.
                if new_class == 'player':
                    raise BadTileError('Player cannot move onto tile at {},{},{}: Tile occupied.'.format(x, y, x))
                elif incumbent_class == 'player':
                    # Robot collision with player; player dies, game over.
                    raise GameOver('You died!')
                elif incumbent_class == 'junk':
                    # Robot collision with junk; robot definitely dies.
                    self.kill(new)
                else:
                    # Robot collision with robot; robots *might* die, unless
                    # incumbent robot has yet to move.
                    # Store the robots in self.to_collide and check again after
                    # all robots have moved.
                    if new not in self.to_collide:
                        self.to_collide[incumbent] = new
                        log('possible collision.')
        if not min(coords) >= 0:
            # This initial sanity check is necessary because negative list
            # indices don't raise an IndexError, but rather return (in this
            # case) undesired results.
            raise BadTileError('Cannot set tile at {},{},{}: Tile not in grid'.format(x, y, z))
        try:
            self._grid[z][y][x] = new
        except IndexError:
            raise BadTileError('Cannot set tile at {},{},{}: Tile not in grid'.format(x, y, z))
        
        if new is not None and new.coords != coords:
            old_coords = new.coords
            new.coords = coords
            self._set_tile(old_coords, None)
    
    def _get_tile(self, coords):
        x, y, z = coords
        try:
            return self._grid[z][y][x]
        except IndexError:
            raise BadTileError('Cannot get tile at {},{},{}: Tile not in grid'.format(x, y, z))
    
    def _get_random_coords(self):
        coords = [
            random.randint(0, self.x-1),
            random.randint(0, self.y-1),
            random.randint(0, self.z-1)
            ]
        return coords
    
    def _get_random_empty_coords(self):
        while True:
            coords = self._get_random_coords()
            if self._tile_is_empty(coords):
                return coords
    
    def _tile_is_empty(self, coords):
        return gameclass(self._get_tile(coords)) == 'empty'
    
    def _grid_is_empty(self):
        return self._grid == self._EMPTY_GRID


class GameGrid(BaseGrid):
    
    """A 3D grid, inheriting from BaseGrid, which has attributes and
    methods required for our game.
    
    This class handles character placement, movement and collision."""
    
    def __init__(self, x, y, z, game):
        self._game = game
        BaseGrid.__init__(self, x, y, z)
    
    def populate(self, enemies):
        self._grid = self._copy_empty_grid()
        _enemies = set()
        while enemies:
            coords = self._get_random_empty_coords()
            robot = Robot(coords, self)
            _enemies.add(robot)
            self._set_tile(coords, robot)
            enemies -= 1
        self._enemies = _enemies
        self._objects = deepcopy(_enemies)
        coords = self._get_random_empty_coords()
        self.player = Player(coords, self)
        self._set_tile(coords, self.player)
        self._objects.add(self.player)
    
    def populate_test(self, enemies):
        self._grid = self._copy_empty_grid()
        _enemies = set()
        coords = self._get_random_empty_coords()
        coords[2] = 4
        robot = Robot(coords, self)
        _enemies.add(robot)
        self._set_tile(coords, robot)
        coords = [c+1 for c in coords]
        coords[2] = 4
        robot = Robot(coords, self)
        _enemies.add(robot)
        self._set_tile(coords, robot)
        self._enemies = _enemies
        self._objects = deepcopy(_enemies)
        coords = self._get_random_empty_coords()
        self.player = Player(coords, self)
        self._set_tile(coords, self.player)
        self._objects.add(self.player)
    
    def collide(self, obj1, obj2, g_cls1=None, g_cls2=None):
        g_cls1 = g_cls1 or gameclass(obj1)
        g_cls2 = g_cls2 or gameclass(obj2)
        log('collision between {} and {}.'.format(obj1, obj2))
        if new_class == 'player':
            raise BadTileError('Player cannot move onto tile at {},{},{}: Tile occupied.'.format(x, y, x))
        elif incumbent_class == 'junk':
            # Robot collision with junk; robot definitely dies.
            self.kill(new)
        elif incumbent_class == 'player':
            # Robot collision with player; player dies, game over.
            raise GameOver('You died!')
    
    def robot_collisions(self):
        # This function goes through to_collide and calls the collision code
        # on a pair of robots where they still occupy the same tile after all
        # robots have moved.
        log(self.to_collide)
        for e in self.to_collide:
            other = self.to_collide[e]
            if e.coords == other.coords:
                log('collision between {} and {}'.format(e, other))
                self.kill(e)
                self.kill(other)
            else:
                log('no collision between {} and {}'.format(e, other))

    def kill(self, enemy):
        enemy.is_alive = False
        self._game.score += enemy.KILLSCORE
        coords = enemy.coords
        j = Junk(coords, self)
        self._set_tile(coords, j)
        self._objects.discard(enemy)
        self._objects.add(j)
        # Killed object is not removed from self._enemies until after
        # all enemies have moved, as the size of the set cannot be changed
        # during iteration.
        
    def move_enemies(self):
        self.to_collide = {}
        for e in self._enemies:
            e.move()
        self.robot_collisions()
        dead_enemies = {e for e in self._enemies if not e.is_alive}
        self._enemies.difference_update(dead_enemies)
        self._objects.difference_update(dead_enemies)
        if not self._enemies:
            raise LevelComplete

    # Player can only view one "floor" of the grid at a time, and always views
    # the grid in plan. Player can cycle between floors at will.
    
    def view_plan(self, elev=None):
        if elev is None:
            elev = self.player.coords[2]
        plan = self._grid[elev]
        return plan
    
