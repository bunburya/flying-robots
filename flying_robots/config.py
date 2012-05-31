from sys import version_info, stderr
from os import mkdir, getenv, name as os_name
from os.path import isdir, isfile, join, expanduser
if version_info.minor >= 2:
    from configparser import ConfigParser, ParsingError
else:
    from .compat import ConfigParser, ParsingError

from .metadata import short_name

if os_name == 'nt':
    CONF_DIR = join(getenv('AppData'), short_name)
elif os_name == 'posix':
    dotconf = expanduser('~/.config')
    if not isdir(dotconf):
        mkdir(dotconf)
    CONF_DIR = join(
            getenv('XDG_CONFIG_HOME', dotconf),
            short_name
            )
else:
    print('Sorry, your operating system is not yet supported.', file=stderr)
    quit(1)

if not isdir(CONF_DIR):
    mkdir(CONF_DIR)

DEFAULT_UI = 'tkinter'
DEFAULT_CTRLSET = 'old'

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
        conf['game']['hiscore'] = 'no'
    except ParsingError as e:
        print('Error parsing config file.')
        print('Error details:', ' '.join(e.args))
        quit(1)

def _get_default_conf(conf, write_to=None):
    x, y, z = 59, 22, 36    # 36-length z-axis gives a total area that is
                            # approximately (area of 2d grid) ** 1.5.
    conf['player'] = {'name': getenv('USER', 'j_doe')}
    conf['game'] = {'start_level': '1', 'hiscore': 'yes', 'max_level': '25'}
    conf['grid'] = {'x': x, 'y': y, 'z': z}

    if write_to is not None:
        with open(write_to, 'w') as f:
            conf.write(f)

def get_config(conf_file=None):
    conf = ConfigParser()
    if conf_file and isfile(conf_file):
        _get_conf_from_file(conf, conf_file)
    else:
        _get_default_conf(conf)
    return conf

def validate_conf(conf):
    grid = conf['grid']
    game = conf['game']
    try:
        grid.getint('x')
        grid.getint('y')
        grid.getint('z')
        game.getint('start_level')
        game.getboolean('hiscore')
    except ValueError as e:
        bad_val = e.args[0].split()[-1]
        print('Invalid configuration option: {}'.format(bad_val),
                file=sys.stderr)
        quit(1)

def apply_opts_to_conf(conf, opts, optmap):
    for o in optmap:
        sect, name, no_hiscore = optmap[o]
        val = getattr(opts, o)
        if val is None:
            continue
        conf[sect][name] = val
        if no_hiscore:
            conf['game']['hiscore'] = 'no'

def write_default_conf():
    conf_file = get_conf_filepath('default.conf')
    _get_default_conf(ConfigParser(), conf_file)
