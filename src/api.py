
import sys
sys.path.append('/usr/lib/mailman')

import simplejson
from bottle import route, run, request, HTTPResponse
from Mailman import Utils, Errors, MailList

from members import Member
from utils import parse_boolean


@route('/', method='GET')
def list_lists():
    response = HTTPResponse(content_type='application/json')

    names = Utils.list_names()
    names.sort()

    response.body = simplejson.dumps(names)
    return response


@route('/<listname>', method='PUT')
def subscribe(listname):
    response = HTTPResponse(content_type='application/json')

    address = request.forms.get('address')
    fullname = request.forms.get('fullname')
    digest = parse_boolean(request.forms.get('digest'))

    try:
        mlist = MailList.MailList(listname)
    except Errors.MMUnknownListError:
        response.status = 404
        response.body = "Unknown Mailing List `{}`.".format(listname)
        return response

    userdesc = Member(fullname, address, digest)
    try:
        mlist.ApprovedAddMember(userdesc, ack=True, admin_notif=True)
    except Errors.MMAlreadyAMember:
        response.status = 409
        response.body = "Address already a member."
    except Errors.MembershipIsBanned as pattern:
        response.status = 403
        response.body = "Banned address."
    except (Errors.MMBadEmailError, Errors.MMHostileAddress):
        response.status = 400
        response.body = "Invalid address."
    else:
        mlist.Save()
        response.body = simplejson.dumps(True)
    finally:
        mlist.Unlock()

    return response


@route('/<listname>', method='DELETE')
def unsubscribe(listname):
    response = HTTPResponse(content_type='application/json')
    address = request.forms.get('address')

    try:
        mlist = MailList.MailList(listname)
    except Errors.MMUnknownListError:
        response.status = 404
        response.body = "Unknown Mailing List `{}`.".format(listname)
        return response

    try:
        mlist.ApprovedDeleteMember(address, admin_notif=False, userack=True)
        mlist.Save()
    except Errors.NotAMemberError:
        response.status = 404
        response.body = "Not a member"
    finally:
        mlist.Unlock()

    response.body = 'true'

    return response


@route('/<listname>', method='GET')
def members(listname):
    response = HTTPResponse(content_type='application/json')

    try:
        mlist = MailList.MailList(listname, lock=False)
    except Errors.MMUnknownListError:
        response.status = 404
        response.body = "Unknown Mailing List `{}`.".format(listname)
        return response

    response.body = simplejson.dumps(mlist.getMembers())
    return response


run(host='0.0.0.0', port=8000, debug=True, reloader=True)
