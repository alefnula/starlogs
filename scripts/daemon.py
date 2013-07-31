#!/usr/bin/env python

__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '31 July 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
import sys

PREFIX = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.extend([
    os.path.join(PREFIX, 'src'),
])

from starlogs.daemon import main

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
