#!/usr/local/bin/python3 -u
#
# The MIT License (MIT)
#
# Copyright (c) 2015 by Oliver Ratzesberger
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# import json
import configparser

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController
from cement.core.exc import CaughtSignal
from cement.ext.ext_colorlog import ColorLogHandler
from cement.ext.ext_configparser import ConfigParserConfigHandler

from rainmachine import __author__, __copyright__, __version__, __license__  # noqa

BANNER = """
rainmachine v%s
%s
""" % (__version__, __copyright__)

DESCRIPTION = """
rainmachine - Backup/Restore utility for rainmachine sprinkler controller.

Simple python utility to back and restore rainmachine configurations to and
from JSON files. Enables you to create a backup of all settings of a rainmachine
controller in order to restore to a new or differnet device. Since the settings
are written as a JSON document, it also enables you to manage and version
control settings of RainMachine controllers instead of having to manipulate
settings through its UI only. """

EPILOG = """

Examples:

$ prainmachine --TBD

Report bugs, submit feature requests, and/or contribute code over at:
https://github.com/fxstein/rainmachine\n
"""

HELP_BACKUP = """
Backup all settings of specified RainMachine controller.
"""
HELP_RESTORE = """
Restore all settings of specified RainMachine controller.
"""
HELP_HOST = """
IP address or hostname of rainmachine controller.
"""
HELP_USER = """
Username of rainmachine controller.
"""
HELP_PASS = """
Password of rainmachine controller.
"""
HELP_FILE = """
Name of backupfile. Default is name of the rainmachine controller.
"""

# Default settings
from cement.utils.misc import init_defaults

defaults = init_defaults('rainmachine', 'rainmachine')
defaults['rainmachine']['tbd'] = False


# Cleanly catch missing mandatory config settings if needed
class RainMachineConfigHandler(ConfigParserConfigHandler):
    class Meta:
        label = 'config_handler'

    def get(self, *args, **kw):
        try:
            return super(RainMachineConfigHandler, self).get(*args, **kw)
        except configparser.Error as e:
            self.app.log.fatal('Missing configuration setting: %s' % e)
            self.app.close(1)


# Define command line options
class RainMachineBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = DESCRIPTION
        epilog = EPILOG
        arguments = [
            (['--host', '--rainmachine'],
             dict(action='store', help=HELP_HOST, dest='host')),
            (['-u', '--user'],
             dict(action='store', help=HELP_USER, dest='user')),
            (['-p', '--password'],
             dict(action='store', help=HELP_PASS, dest='pass')),
            (['-b', '--backup'],
             dict(action='store_true', help=HELP_BACKUP, dest='backup')),
            (['-r', '--restore'],
             dict(action='store_true', help=HELP_RESTORE, dest='restore')),
            (['-f', '--file'],
             dict(action='store', help=HELP_FILE, dest='file')),
            (['-v', '--version'], dict(action='version', version=BANNER)),
            ]


# Colors for logging
COLORS = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'white,bg_red',
}


# The main app of pubkey
class RainMachineApp(CementApp):
    class Meta:
        label = 'rainmachine'
        config_defaults = defaults

        base_controller = 'base'
        config_handler = 'config_handler'
        handlers = [RainMachineBaseController, RainMachineConfigHandler]

        extensions = ['colorlog']
        arguments_override_config = True

        log_handler = ColorLogHandler(colors=COLORS)

    def setup(self):
        # always run core setup first
        super(RainMachineApp, self).setup()

        self.log.debug('running setup()')


with RainMachineApp() as app:
    app.run()

    try:
        app.run_forever()
    except (KeyboardInterrupt, SystemExit, CaughtSignal):
        pass
