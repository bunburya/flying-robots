from os import mkdir, getenv
from os.path import isdir, isfile, join, expanduser
from configparser import ConfigParser, ParsingError

from debug import log

CONF_DIR = expanduser('~/.flying_robots')
if not isdir(CONF_DIR):
    mkdir(CONF_DIR)
    
def get_conf_filepath(filename):
    """Takes a filename as an argument, returns the full path to that file,
    which is the filename joined with the config directory."""
    return join(CONF_DIR, filename)

def calc_enemies(level):
    # bsd-robots has 10*lvl enemies on each level.
    # We're just going to take that ** 1.5, for now at least.
    return int((10 * level) ** 1.5)

def _get_conf_from_file(conf, f):
    try:
        conf.read(f)
    except ParsingError as e:
        print('Error parsing config file.')
        print('Error details:', ' '.join(e.args))
        quit(1)

def _get_default_conf(conf, write_to=None):
    x, y, z = 59, 22, 36    # 36-length z-axis gives a total area that is
                            # approximately (area of 2d grid) ** 1.5.
    conf['player'] = {'name': getenv('USER', 'j_doe')}
    conf['game'] = {'start_level': '1'}
    conf['size'] = {'x': x, 'y': y, 'z': z}
    conf['view'] = {
        'zoom_to_player_on_move': 'yes',
        'zoom_to_player_on_teleport': 'yes'
        }
    if write_to is not None:
        with open(write_to, 'w') as f:
            conf.write(f)

def write_default_conf():
    conf_file = get_conf_filepath('default.conf')
    _get_default_conf(ConfigParser(), conf_file)

def get_config(conf_file=None):
    conf = ConfigParser()
    if conf_file and isfile(conf_file):
        _get_conf_from_file(conf)
    else:
        _get_default_conf(conf)
    return conf
