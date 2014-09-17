#!/usr/bin/env python

import sys

from optparse import OptionParser

from bottle import run


def parse_options():
    parser = OptionParser()
    parser.add_option("-b", "--bind", dest="bind", default='127.0.0.1:8000',
                      help="Bind address. Default: '127.0.0.1:8000'.")
    parser.add_option("--allow-from", action="append",
                      default=['127.0.0.1'], dest="allow_from",
                      help=("IPs to allow incoming requests. By deufalt only "
                            "allow connections from '127.0.0.1'."))
    parser.add_option("-l", "--mailman-lib-path", dest="mailmanlib_path",
                      default='/usr/lib/mailman',
                      help=("Path to mailman libs directory. "
                            "Default: '/usr/lib/mailman'."))
    parser.add_option("-d", "--debug", action="store_true", default=False,
                      help="Print debug information")

    (options, args) = parser.parse_args()
    return options


if __name__ == '__main__':
    opt = parse_options()

    # Add mailman to path
    #   Must be done before importing get_application
    sys.path.append(opt.mailmanlib_path)

    from mailmanapi.api import get_application
    application = get_application(opt.allow_from)

    host, port = opt.bind.split(':')

    run(application, host=host, port=port, debug=opt.debug, server='paste')
