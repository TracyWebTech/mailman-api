
import sys
sys.path.append('/usr/lib/mailman')

from bottle import route, run, request
from Mailman import Utils, Errors

from members import Member
from utils import parse_boolean, jsonify, get_mailinglist


@route('/', method='GET')
def list_lists():
    all_lists = Utils.list_names()
    lists = []

    address = request.query.get('address')
    if address:
        for listname in all_lists:
            mlist = get_mailinglist(listname, lock=False)
            members = mlist.getMembers()
            if address in members:
                lists.append(listname)
    else:
        lists = all_lists

    return jsonify(lists)


@route('/<listname>', method='PUT')
def subscribe(listname):
    address = request.forms.get('address')
    fullname = request.forms.get('fullname')
    digest = parse_boolean(request.forms.get('digest'))

    mlist = get_mailinglist(listname)
    userdesc = Member(fullname, address, digest)

    try:
        mlist.ApprovedAddMember(userdesc, ack=True, admin_notif=True)
    except Errors.MMAlreadyAMember:
        return jsonify("Address already a member.", 409)
    except Errors.MembershipIsBanned as pattern:
        return jsonify("Banned address.", 403)
    except (Errors.MMBadEmailError, Errors.MMHostileAddress):
        return jsonify("Invalid address.", 400)

    else:
        mlist.Save()
    finally:
        mlist.Unlock()

    return jsonify(True)


@route('/<listname>', method='DELETE')
def unsubscribe(listname):
    address = request.forms.get('address')
    mlist = get_mailinglist(listname)

    try:
        mlist.ApprovedDeleteMember(address, admin_notif=False, userack=True)
        mlist.Save()
    except Errors.NotAMemberError:
        return jsonify("Not a member.", 404)
    finally:
        mlist.Unlock()

    return jsonify(True)


@route('/<listname>', method='GET')
def members(listname):
    mlist = get_mailinglist(listname, lock=False)
    return jsonify(mlist.getMembers())


run(host='0.0.0.0', port=8000, debug=True, reloader=True)
