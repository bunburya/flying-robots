#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import version_info
if version_info.minor < 2:
    from optparse import OptionParser as ArgumentParser
else:
    from argparse import ArgumentParser

import ui
from config import get_config

parser = ArgumentParser()
parser.add_argument('-c', '--config', dest='conf_file',
                  help='provide a custom configuration file', metavar='FILE')
parser.add_argument('-l', '--level', dest='start_level',
                  help='start playing at the specified level', metavar='LEVEL')
parser.add_argument('-n', '--name', dest='name',
                  help='specify player name', metavar='NAME')

options = parser.parse_args()
conf = get_config(options)

ui.GameInterface(conf)
