import os
import uuid

from .utils import (parse_boolean, jsonify, get_mailinglist,
                    get_timestamp, get_public_attributes)
from Mailman import (Errors, Post, mm_cfg, UserDesc,
                     MailList, Utils, Defaults)
from bottle import request, template

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
    'BadListNameError': 9,
    'AssertionError': 10,
    'InvalidPassword': 11,
    'MMUnknownListError': 12,
    'MMListAlreadyExistsError': 13,
    'InvalidParams': 14,
}


def list_lists():
    """Lists existing mailing lists on the server.

    **Method**: GET

    **URI**: /v2/

    Returns a list of dictionaries the mailing lists and its public attributes
    that exist on this server."""

    all_lists = Utils.list_names()
    lists = []

    address = request.query.get('address')
    for listname in all_lists:
        if listname == Defaults.MAILMAN_SITE_LIST:
            continue

        mlist = get_mailinglist(listname, lock=False)

        members = mlist.getMembers()
        if not address or address in members:
            list_values = get_public_attributes(mlist)
            list_values["listname"] = listname

            lists.append(list_values)

    return jsonify(lists)


def subscribe(listname):
    """Adds a new subscriber to the list called `<listname>`

    **Method**: PUT

    **URI**: /v2/subscribe/<listname>

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
    """Unsubscribe an email address from the mailing list.

    **Method**: DELETE

    **URI**: /v2/subscribe/<listname>

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

    **URI**: /v2/sendmail/<listname>

    **Parameters**:

      * `name_from`: name of the poster
      * `email_from`: email address of the poster
      * `subject`: the subject of the message
      * `body`: the body of the message.
      * `in_reply_to` (optional): Message-ID of the message that is being
        replied to, if any."""

    try:
        mlist = MailList.MailList(listname, lock=False)
    except Errors.MMUnknownListError, e:
        return jsonify(ERRORS_CODE[e.__class__.__name__])

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


def create_list(listname):
    """Create an email list.

    **Method**: POST

    **URI**: /v2/lists/<listname>

    **Parameters**:

      * `admin`: email of list admin
      * `password`: list admin password
      * `subscribe_policy`: 1) Confirm; 2) Approval; 3)Confirm and approval.
      Default is Confirm (1)
      * `archive_private`: 0) Public; 1) Private. Default is Public (0) """
    admin = request.forms.get('admin')
    password = request.forms.get('password')
    subscribe_policy = request.forms.get('subscribe_policy', 1)
    archive_private = request.forms.get('archive_private', 0)

    try:
        subscribe_policy = int(subscribe_policy)
        archive_private = int(archive_private)
    except ValueError:
        return jsonify(ERRORS_CODE['InvalidParams'])

    if subscribe_policy < 1 or subscribe_policy > 3:
        subscribe_policy = 1

    if archive_private < 0 or archive_private > 1:
        archive_private = 0

    result = jsonify(ERRORS_CODE['Ok'])

    if password == '':
        return jsonify(ERRORS_CODE['InvalidPassword'])
    else:
        password = Utils.sha_new(password).hexdigest()

    mail_list = MailList.MailList()
    try:
        mail_list.Create(listname, admin, password)
        mail_list.archive_private = archive_private
        mail_list.subscribe_policy = subscribe_policy
        mail_list.Save()
    except (Errors.BadListNameError, AssertionError,
            Errors.MMBadEmailError, Errors.MMListAlreadyExistsError), e:
        result = jsonify(ERRORS_CODE[e.__class__.__name__])
    finally:
        mail_list.Unlock()
    return result


def members(listname):
    """Lists subscribers for the `listname` list.

    **Method**: GET

    **URI**: /v2/members/<listname>

    Returns an array of email addresses."""

    try:
        mlist = MailList.MailList(listname.lower(), lock=False)
    except Errors.MMUnknownListError, e:
        return jsonify(ERRORS_CODE[e.__class__.__name__])
    return jsonify(mlist.getMembers())
