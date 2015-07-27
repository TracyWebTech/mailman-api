import os
import uuid
import logging

from bottle import route, request, template, default_app

try:
    from Mailman import Utils, Errors, Post, mm_cfg, UserDesc
except ImportError:
    logging.error('Could not import Mailman module')

from .utils import parse_boolean, jsonify, get_mailinglist, get_timestamp


CWD = os.path.abspath(os.path.dirname(__file__))
EMAIL_TEMPLATE = os.path.join(CWD, 'templates', 'message.tpl')

ERRORS_CODE = {
    'Ok': 0,
    'MMSubscribeNeedsConfirmation': 1,
    'MMNeedApproval': 2,
    'MMAlreadyAMember': 3,
    'MembershipIsBanned': 4,
    'MMBadEmailError': 5,
    'MMHostileAddress': 6,
    'NotAMemberError': 7,
    'MissingInformation': 8,
}


def subscribe(listname):
    """Adds a new subscriber to the list called `<listname>`

    **Method**: PUT

    **URI**: /<listname>

    **Parameters**:

      * `address`: email address that is to be subscribed to the list.
      * `fullname`: full name of the person being subscribed to the list.
      * `digest`: if this equals `true`, the new subscriber will receive
        digests instead of every mail sent to the list.

    """

    address = request.forms.get('address')
    fullname = request.forms.get('fullname')
    digest = parse_boolean(request.forms.get('digest'))

    mlist = get_mailinglist(listname)
    userdesc = UserDesc.UserDesc(address, fullname, digest=digest)
    result = jsonify(ERRORS_CODE['Ok'])

    try:
        mlist.AddMember(userdesc)
    except (Errors.MMSubscribeNeedsConfirmation,
            Errors.MMNeedApproval,
            Errors.MMAlreadyAMember,
            Errors.MembershipIsBanned,
            Errors.MMBadEmailError,
            Errors.MMHostileAddress), e:
        result = jsonify(ERRORS_CODE[e.__class__.__name__])
    finally:
        mlist.Save()
        mlist.Unlock()

    return result


def unsubscribe(listname):
    """Unsubsribe an email address from the mailing list.

    **Method**: DELETE

    **URI**: /<listname>

    **Parameters**:

      * `address`: email address that is to be unsubscribed from the list

    """

    address = request.forms.get('address')
    mlist = get_mailinglist(listname)
    result = jsonify(ERRORS_CODE['Ok'])

    try:
        mlist.ApprovedDeleteMember(address, admin_notif=False, userack=True)
    except Errors.NotAMemberError, e:
        result = jsonify(ERRORS_CODE[e.__class__.__name__])
    finally:
        mlist.Save()
        mlist.Unlock()

    return result


def sendmail(listname):
    """Posts an email to the mailing list.

    **Method**: POST

    **URI**: /<listname>/sendmail

    **Parameters**:

      * `name_from`: name of the poster
      * `email_from`: email address of the poster
      * `subject`: the subject of the message
      * `body`: the body of the message.
      * `in_reply_to` (optional): Message-ID of the message that is being
        replied to, if any."""

    mlist = get_mailinglist(listname, lock=False)

    context = {}
    context['email_to'] = mlist.GetListEmail()
    context['message_id'] = uuid.uuid1()
    context['ip_from'] = request.environ.get('REMOTE_ADDR')
    context['timestamp'] = get_timestamp()

    context['name_from'] = request.forms.get('name_from')
    context['email_from'] = request.forms.get('email_from')
    context['subject'] = request.forms.get('subject')
    context['body'] = request.forms.get('body')

    in_reply_to = request.forms.get('in_reply_to')
    if in_reply_to:
        context['in_reply_to'] = in_reply_to

    result = jsonify(ERRORS_CODE['Ok'])

    if None in context.values():
        result = jsonify(ERRORS_CODE['MissingInformation'])

    email = template(EMAIL_TEMPLATE, context)
    Post.inject(listname, email.encode('utf8'), qdir=mm_cfg.INQUEUE_DIR)
    return result