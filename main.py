#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from optparse import OptionParser

import ui
from config import get_config

parser = OptionParser()
parser.add_option('-c', '--config', dest='conf_file',
                  help='provide a custom configuration file', metavar='FILE')
parser.add_option('-l', '--level', dest='start_level',
                  help='start playing at the specified level', metavar='LEVEL')
parser.add_option('-n', '--name', dest='name',
                  help='specify player name', metavar='NAME')

options, args = parser.parse_args()
conf = get_config(options)

ui.GameInterface(conf)
