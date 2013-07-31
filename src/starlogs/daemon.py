__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '31 July 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'


#!/usr/bin/env python

import sys
from optparse import OptionParser
# tea imports
from tea.utils.daemon import Daemon
# board imports
from starlogs.server import main as server_main


class StarlogsDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        self.port = kwargs.pop('port', None)
        super(StarlogsDaemon, self).__init__(*args, **kwargs)

    def run(self, *args):
        server_main(port=self.port, debug=False)


def main(args):
    parser = OptionParser(usage="usage: %prog [options] start|stop|restart", version="%prog 0.1")
    parser.add_option('-p', '--port', dest='port', action='store', type='int', default=None)
    options, args = parser.parse_args(args)

    if len(args) != 1 or args[0] not in ('start', 'stop', 'restart'):
        parser.error('Invalid command.')

    daemon = StarlogsDaemon('/var/tmp/starlogs.pid', port=options.port)
    if args[0] == 'start':
        print 'Starting starlogs...'
        daemon.start()
    if args[0] == 'stop':
        print 'Stopping starlogs...'
        daemon.stop()
    if args[0] == 'restart':
        daemon.stop()
        daemon.start()
    sys.exit(0)
