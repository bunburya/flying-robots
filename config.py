from os import mkdir
from os.path import isdir, isfile, join, expanduser
from configparser import ConfigParser, ParsingError

from debug import log

CONF_DIR = expanduser('~/.flying_robots')
if not isdir(CONF_DIR):
    mkdir(CONF_DIR)
CONF_FILE = join(CONF_DIR, 'config')

conf = ConfigParser()

def calc_enemies(level):
    # bsd-robots has 10*lvl enemies on each level.
    # We're just going to take that ** 1.5, for now at least.
    return int((10 * level) ** 1.5)

def _get_conf_from_file(conf, f=CONF_FILE):
    try:
        conf.read(CONF_FILE)
    except ParsingError as e:
        print('Error parsing config file.')
        print('Error details:', ' '.join(e.args))
        quit(1)

def _get_default_conf(conf, write_to=CONF_FILE):
    x, y, z = 59, 22, 36    # 36-length z-axis gives a total area that is
                            # approximately (area of 2d grid) ** 1.5.
    conf['size'] = {'x': x, 'y': y, 'z': z}
    conf['view'] = {
        'zoom_to_player_on_move': 'yes',
        'zoom_to_player_on_teleport': 'yes'
        }
    if write_to is not None:
        with open(write_to, 'w') as f:
            conf.write(f)

def get_config():
    conf = ConfigParser()
    if isfile(CONF_FILE):
        _get_conf_from_file(conf)
    else:
        _get_default_conf(conf)
    return conf
