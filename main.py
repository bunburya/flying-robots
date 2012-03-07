#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import version_info
if version_info.minor < 2:
    from _optparse import ArgumentParser
else:
    from argparse import ArgumentParser
from curses import wrapper

import ui
from config import get_config, apply_opts_to_conf

parser = ArgumentParser()
parser.add_argument('-c', '--config', dest='conf_file',
                  help='provide a custom configuration file', metavar='FILE')
parser.add_argument('-l', '--level', dest='start_level',
                  help='start playing at the specified level', metavar='LEVEL')
parser.add_argument('-n', '--name', dest='name',
                  help='specify player name', metavar='NAME')
parser.add_argument('-x', dest='x', help='specify length on x-axis of grid',
                    metavar='N')
parser.add_argument('-y', dest='y', help='specify length on y-axis of grid',
                    metavar='N')
parser.add_argument('-z', dest='z', help='specify length on z-axis of grid',
                    metavar='N')

options = parser.parse_args()
conf = get_config(options.conf_file)

# Each key in this dict is the name of the relevant attribute in the options
# object returned by parser.parse_args.
# Each value is a 3-tuple containing the name of the section in the config
# containing the setting, the name of the setting itself, and a boolean value
# indicating whether changing this setting precludes the score from this game
# from being counted towards the high scores (True if it does).
optmap = {
    'name':         ('player', 'name', False),
    'start_level':  ('game', 'start_level', True),
    'x':            ('grid', 'x', True),
    'y':            ('grid', 'y', True),
    'z':            ('grid', 'z', True)
    }

apply_opts_to_conf(conf, options, optmap)

wrapper(lambda s: ui.GameInterface(s, conf))
