from os import mkdir
from os.path import isdir, isfile, join, expanduser
from configparser import ConfigParser, ParsingError

CONF_DIR = expanduser('~/.flying_robots')
if not isdir(CONF_DIR):
    mkdir(CONF_DIR)
CONF_FILE = join(CONF_DIR, 'config')

conf = ConfigParser()

def get_conf_from_file(conf, f=CONF_FILE):
    try:
        conf.read(CONF_FILE)
    except ParsingError as e:
        print('Error parsing config file.')
        print('Error details:', ' '.join(e.args))
        quit(1)

def get_default_conf(conf, write_to=CONF_FILE):
    x, y, z = 59, 22, 22
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
        get_conf_from_file(conf)
    else:
        get_default_conf(conf)
    return conf
