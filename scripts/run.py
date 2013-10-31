#!/usr/bin/env python

import os
CWD = os.path.abspath(os.path.dirname(__file__))

import sys
sys.path.append('/usr/lib/mailman')
sys.path.append(os.path.abspath(os.path.join(CWD, '..')))


import bottle
from paste import httpserver
from mailmanapi import *
from mailmanapi.settings import ALLOWED_IPS


bottle_app = bottle.default_app()
def application(environ, start_response):
    if environ['REMOTE_ADDR'] not in ALLOWED_IPS:
        status = '403 FORBIDDEN'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return 'FORBIDDEN'

    return bottle_app(environ, start_response)

httpserver.serve(application, host='0.0.0.0', port=8000)
