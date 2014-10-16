

import json
import logging

from time import strftime

from bottle import HTTPResponse

try:
    from Mailman import MailList, Errors
except ImportError:
    logging.error('Could not import Mailman module')


def parse_boolean(value):
    if value and value.lower() == 'true':
        return True

    return False


def jsonify(body='', status=200):
    response = HTTPResponse(content_type='application/json')
    response.body = json.dumps(body)
    response.status = status
    return response


def get_mailinglist(listname, lock=True):
    try:
        return MailList.MailList(listname, lock=lock)
    except Errors.MMUnknownListError:
        raise jsonify("Unknown Mailing List `{}`.".format(listname), 404)


def get_timestamp():
    return strftime('%a, %d %b %Y %H:%M:%S %z (%Z)')
