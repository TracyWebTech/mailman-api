
import os
import uuid

from bottle import route, request, template
from Mailman import Utils, Errors, Post, mm_cfg

from members import Member
from utils import parse_boolean, jsonify, get_mailinglist, get_timestamp


CWD = os.path.abspath(os.path.dirname(__file__))
EMAIL_TEMPLATE = os.path.join(CWD, 'templates', 'message.tpl')


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


@route('/<listname>/sendmail', method='POST')
def sendmail(listname):
    mlist = get_mailinglist(listname, lock=False)

    context = {}
    context['email_to'] = mlist.GetListEmail()
    context['message_id'] = uuid.uuid1()
    context['ip_from'] = request.environ.get('REMOTE_ADDR')
    context['timestamp'] = get_timestamp()

    context['email_from'] = request.forms.get('from')
    context['subject'] = request.forms.get('subject')
    context['body'] = request.forms.get('body')

    if None in context.values():
        return jsonify('Missing information. `from`, `subject` and `body` '
                       'are mandatory', 400)

    email = template(EMAIL_TEMPLATE, context)
    Post.inject(listname, email.encode('utf8'), mm_cfg.INQUEUE_DIR)
    return jsonify(True)

