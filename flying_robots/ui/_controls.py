control_help = """CONTROLS

{nw} {n} {ne}
 \|/
{w}-{x}-{e}
 /|\
{sw} {s} {se}

Holding shift while pressing any of the above also moves up the z-axis.
Holding ctrl while pressing any of the above also moves down the z-axis.

{tele} = Teleport to random location.
{wait} = Stay where you are and pass turns until you complete the level or die.
    You get a 10% bonus to score for each robot who dies in this period,
    but it only counts if you complete the level.
{sticky} = Toggle "sticky" mode, in which your view stays fixed on the current
    elevation even when you move.
{afap} = Toggle "as-far-as-possible" mode. When you press a movement key while in
    this mode, you move as far as is safe in that direction.
    This mode is unset after each turn.
{quit} = Quit.

{pgup} = View next level on z-axis, without moving.
{pgup} = View previous level on z-axis, without moving.
{player} = View level on z-axis on which player is placed, without moving.
{goto} = Prompt for number of level on z-axis and view that level, without moving.
"""

def _invert_dict(d):
    return dict(zip(d.values(), d.keys()))

class ControlSet:
    
    """A class which represents a set of game controls and contains associated
    methods and data
    
    In order to have control sets that work across several UI libraries,
    special keys (like Page Up) are represented by short strings which we will
    call symbols (like "pgup" for Page Up). The ControlSet class contains a
    dict mapping symbols to their corresponding UI-specific values, and vice
    versa.
    
    When a ControlSet instance is initialized, a dict is provided which maps
    symbols to their UI-specific values. After move keys and special command
    keys are added, the ControlSet instance contains 4 important pieces of
    information:
    
    self.move_syms, containing the move keys displayed as symbols where
        appropriate;
    self.move_keys, containing the move keys displayed as UI-specific values
        where appropriate;
    self.special_syms, containing the special command keys displayed as symbols
        where appropriate; and
    self.special_keys, containing the special command keys displayed as symbols
        where appropriate.
        
    """
    
    _control_help = control_help
    
    xy_move_keys = {
        'w':    (-1, 0),
        's':    (0, 1),
        'n':    (0, -1),
        'e':    (1, 0),
        'sw':    (-1, 1),
        'se':    (1, 1),
        'nw':    (-1, -1),
        'ne':    (1, -1),
        'x':    (0, 0)
        }
    
    special_cmds = {
        'tele',
        'wait',
        'next',
        'prev',
        'player',
        'goto',
        'sticky',
        'afap',
        'quit'
        }
        
    def __init__(self, keys):
                
        self.sym_to_key = keys
        self.key_to_sym = _invert_dict(keys)
        self.add_move_keys(self.move_keys)
        self.add_special_keys(self.special_keys)
    
    def _conv_keymap(self, keymap):
        """Takes a dict, converts symbols ("pgup" etc) to their corresponding
        values, and returns the converted dict.
        """
        _keymap = {}
        for sym in keymap:
            key = self.sym_to_key.get(sym, sym)
            _keymap[key] = keymap[sym]
        return _keymap
    
    def add_move_keys(self, keymap):
        """Takes a dict mapping keys (symbols as apt) to movement commands"""
        self.move_syms_to_cmds = keymap
        self.move_cmds_to_syms = _invert_dict(keymap)
        keys = self._conv_keymap(keymap)
        self.move_keys_to_cmds = keys
        self.move_cmds_to_keys = _invert_dict(keys)
    
    def add_special_keys(self, keymap):
        """Takes a dict mapping keys (symbols as apt) to special commands"""
        self.special_syms_to_cmds = keymap
        self.special_cmds_to_syms = _invert_dict(keymap)
        keys = self._conv_keymap(keymap)
        self.special_keys_to_cmds = keys
        self.special_cmds_to_keys = _invert_dict(keys)
    
    def get_move_xy(self, key):
        return self.xy_move_keys[self.move_keys[key]]

    def is_move_key(self, key):
        return key in self.move_keys_to_cmds
    
    @property
    def control_help(self):
        all_ctrls = {}
        all_ctrls.update(self.move_cmds_to_syms)
        all_ctrls.update(self.special_cmds_to_syms)
        return self._control_help.format(all_ctrls)

class ClassicControls(ControlSet):

    move_keys = {
        'k':    'n',
        'h':    'w',
        'l':    'e',
        'j':    's',
        'y':    'nw',
        'u':    'ne',
        'b':    'sw',
        'n':    'se'
        }

    special_keys = {
        't':    'tele',
        'w':    'wait',
        'pgup': 'next',
        'pgdn': 'prev',
        'g':    'goto',
        'p':    'player',
        's':    'sticky',
        'f':    'afap',
        'q':    'quit'
        }
