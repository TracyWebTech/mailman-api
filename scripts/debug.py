#!/usr/bin/env python

import sys
sys.path.append('/usr/lib/mailman')
sys.path.append('..')

from mailmanapi import *
from bottle import run

run(host='0.0.0.0', port=8000, debug=True, reloader=True)
